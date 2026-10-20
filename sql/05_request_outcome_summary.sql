-- 05: Service Request Resolution Analysis
-- Purpose: Calculate request-level resolution rates, unresolved requests, and average referrals per request across all service categories.
-- A request counts as successful if at least one associated referral has the outcome 'Needs Met'.

WITH request_summary AS (
    SELECT
        sr.request_id,
        sr.service_category,
        sr.region,
        sr.urgency_level,

        MAX(CASE
            WHEN ro.outcome_status = 'Needs Met'
            THEN 1 ELSE 0
        END) AS has_success,

        MAX(CASE
            WHEN ro.outcome_status = 'Unsuccessful'
            THEN 1 ELSE 0
        END) AS has_failure,

        COUNT(DISTINCT r.referral_id) AS referral_count

    FROM service_requests sr

    LEFT JOIN referrals r
        ON sr.request_id = r.request_id

    LEFT JOIN referral_outcomes ro
        ON r.referral_id = ro.referral_id

    GROUP BY
        sr.request_id,
        sr.service_category,
        sr.region,
        sr.urgency_level
)
SELECT
    service_category,

    COUNT(*) AS total_requests,

    SUM(has_success) AS resolved_requests,

    SUM(CASE
        WHEN has_success = 0
        THEN 1 ELSE 0
    END) AS without_recorded_success,

    ROUND(
        100.0 * SUM(has_success) / COUNT(*),
        2
    ) AS resolution_rate_pct,

    ROUND(
        AVG(referral_count),
        2
    ) AS avg_referrals_per_request

FROM request_summary

GROUP BY service_category
ORDER BY resolution_rate_pct DESC;
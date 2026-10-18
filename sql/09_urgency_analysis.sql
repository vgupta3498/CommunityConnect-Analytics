-- 09: Urgency-Level Resolution Analysis
-- Compares request resolution rates by urgency level.
-- Counts each request once, regardless of referral count.

WITH request_summary AS (
    SELECT
        sr.request_id,
        sr.urgency_level,

        MAX(CASE
            WHEN ro.outcome_status = 'Needs Met'
            THEN 1 ELSE 0
        END) AS has_success

    FROM service_requests sr

    LEFT JOIN referrals r
        ON sr.request_id = r.request_id

    LEFT JOIN referral_outcomes ro
        ON r.referral_id = ro.referral_id

    GROUP BY sr.request_id, sr.urgency_level
)

SELECT
    urgency_level,
    COUNT(*) AS total_requests,
    SUM(has_success) AS resolved_requests,

    COUNT(*) - SUM(has_success)
        AS without_recorded_success,

    ROUND(
        100.0 * SUM(has_success) / COUNT(*),
        2
    ) AS resolution_rate_pct

FROM request_summary

GROUP BY urgency_level
ORDER BY resolution_rate_pct ASC;
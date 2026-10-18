-- 08: Regional Performance Analysis
-- Compares request resolution rates across regions.
-- Counts a request as successful if at least one referral is 'Needs Met'.

WITH request_summary AS (
    SELECT
        sr.request_id,
        sr.region,

        MAX(CASE
            WHEN ro.outcome_status = 'Needs Met'
            THEN 1 ELSE 0
        END) AS has_success

    FROM service_requests sr

    LEFT JOIN referrals r
        ON sr.request_id = r.request_id

    LEFT JOIN referral_outcomes ro
        ON r.referral_id = ro.referral_id

    GROUP BY sr.request_id, sr.region
)

SELECT
    region,
    COUNT(*) AS total_requests,
    SUM(has_success) AS resolved_requests,

    COUNT(*) - SUM(has_success)
        AS without_recorded_success,

    ROUND(
        100.0 * SUM(has_success) / COUNT(*),
        2
    ) AS resolution_rate_pct

FROM request_summary

GROUP BY region
ORDER BY resolution_rate_pct ASC;
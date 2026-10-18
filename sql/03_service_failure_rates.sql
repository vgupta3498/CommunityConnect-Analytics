
-- Analysis: Overall referral failure rate by service
-- Purpose: Compare unsuccessful referral rates across all six service categories.

SELECT
    s.service_category,

    COUNT(*) AS total_referrals,

    SUM(
        CASE
            WHEN o.outcome_status = 'Unsuccessful'
            THEN 1
            ELSE 0
        END
    ) AS unsuccessful_referrals,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN o.outcome_status = 'Unsuccessful'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS failure_rate_pct

FROM referrals AS r

JOIN service_requests AS s
    ON r.request_id = s.request_id

LEFT JOIN referral_outcomes AS o
    ON r.referral_id = o.referral_id

GROUP BY s.service_category

ORDER BY failure_rate_pct DESC;

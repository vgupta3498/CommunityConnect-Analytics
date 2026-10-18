-- 07: Pending and Unknown Referral Outcomes
-- Identifies unresolved or missing outcomes by service category.
-- Helps detect follow-up gaps and incomplete records.

SELECT
    sr.service_category,

    COUNT(DISTINCT r.referral_id) AS total_referrals,

    SUM(CASE
        WHEN ro.outcome_status = 'Pending'
        THEN 1 ELSE 0
    END) AS pending_referrals,

    SUM(CASE
        WHEN ro.outcome_status = 'Unknown'
        THEN 1 ELSE 0
    END) AS unknown_referrals,

    SUM(CASE
        WHEN ro.outcome_status IS NULL
        THEN 1 ELSE 0
    END) AS missing_outcomes,

    ROUND(
        100.0 * SUM(CASE
            WHEN ro.outcome_status IN ('Pending', 'Unknown')
                 OR ro.outcome_status IS NULL
            THEN 1 ELSE 0
        END) / COUNT(DISTINCT r.referral_id),
        2
    ) AS unresolved_pct

FROM referrals r

JOIN service_requests sr
    ON r.request_id = sr.request_id

LEFT JOIN referral_outcomes ro
    ON r.referral_id = ro.referral_id

GROUP BY sr.service_category

ORDER BY unresolved_pct DESC;
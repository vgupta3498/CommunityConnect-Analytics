-- 10: Provider Performance Analysis
-- Compares referral failure rates across providers.
-- Includes referral volume to support fair comparisons.

SELECT
    p.provider_id,
    p.provider_name,

    COUNT(DISTINCT r.referral_id) AS total_referrals,

    COUNT(DISTINCT CASE
        WHEN ro.outcome_status = 'Needs Met'
        THEN r.referral_id
    END) AS successful_referrals,

    COUNT(DISTINCT CASE
        WHEN ro.outcome_status = 'Unsuccessful'
        THEN r.referral_id
    END) AS unsuccessful_referrals,

    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN ro.outcome_status = 'Unsuccessful'
            THEN r.referral_id
        END) / NULLIF(COUNT(DISTINCT r.referral_id), 0),
        2
    ) AS failure_rate_pct

FROM providers p

LEFT JOIN referrals r
    ON p.provider_id = r.provider_id

LEFT JOIN referral_outcomes ro
    ON r.referral_id = ro.referral_id

GROUP BY p.provider_id, p.provider_name

HAVING COUNT(DISTINCT r.referral_id) >= 30

ORDER BY failure_rate_pct DESC
LIMIT 10;
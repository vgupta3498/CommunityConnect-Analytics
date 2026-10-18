
-- Project: CommunityConnect Analytics
-- Purpose: Identify rental assistance referrals recorded as unsuccessful due to unavailable funding.

SELECT
    r.referral_id,
    s.service_category,
    p.provider_name,
    o.outcome_status,
    o.failure_reason

FROM referrals AS r

JOIN service_requests AS s
    ON r.request_id = s.request_id

JOIN providers AS p
    ON r.provider_id = p.provider_id

JOIN referral_outcomes AS o
    ON r.referral_id = o.referral_id

WHERE s.service_category = 'Rental Assistance'
  AND o.outcome_status = 'Unsuccessful'
  AND o.failure_reason = 'Funding Unavailable'

LIMIT 20;


-- Analysis 2: Count funding-related failures by provider
-- Business question: Which providers have the highest number of rental assistance funding failures? or Which providers have the most funding-related failures?

SELECT
    p.provider_name,
    COUNT(*) AS funding_failure_count

FROM referrals AS r

JOIN service_requests AS s
    ON r.request_id = s.request_id

JOIN providers AS p
    ON r.provider_id = p.provider_id

JOIN referral_outcomes AS o
    ON r.referral_id = o.referral_id

WHERE s.service_category = 'Rental Assistance'
  AND o.outcome_status = 'Unsuccessful'
  AND o.failure_reason = 'Funding Unavailable'

GROUP BY p.provider_id, p.provider_name

ORDER BY funding_failure_count DESC

LIMIT 10;



-- Analysis 3: Funding-related failure rate by provider
-- Purpose: Compare funding failures against total rental assistance referrals received? or What percentage of each provider's rental referrals failed because of unavailable funding?

SELECT
    p.provider_name,

    COUNT(*) AS total_referrals,

    SUM(
        CASE
            WHEN o.outcome_status = 'Unsuccessful'
             AND o.failure_reason = 'Funding Unavailable'
            THEN 1
            ELSE 0
        END
    ) AS funding_failures,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN o.outcome_status = 'Unsuccessful'
                 AND o.failure_reason = 'Funding Unavailable'
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS funding_failure_rate_pct

FROM referrals AS r

JOIN service_requests AS s
    ON r.request_id = s.request_id

JOIN providers AS p
    ON r.provider_id = p.provider_id

LEFT JOIN referral_outcomes AS o
    ON r.referral_id = o.referral_id

WHERE s.service_category = 'Rental Assistance'

GROUP BY p.provider_id, p.provider_name

ORDER BY funding_failure_rate_pct DESC;

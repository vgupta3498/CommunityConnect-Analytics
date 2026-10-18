-- Analysis: Failure reasons across all service categories
-- Purpose: Identify why referrals are unsuccessful.

SELECT
    s.service_category,
    o.failure_reason,
    COUNT(*) AS failure_count

FROM referrals AS r

JOIN service_requests AS s
    ON r.request_id = s.request_id

JOIN referral_outcomes AS o
    ON r.referral_id = o.referral_id

WHERE o.outcome_status = 'Unsuccessful'

GROUP BY
    s.service_category,
    o.failure_reason

ORDER BY
    s.service_category,
    failure_count DESC;

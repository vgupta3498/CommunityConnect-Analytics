-- 11: Data Quality and Relationship Checks
-- Identifies missing fields and broken table relationships.
-- Validates data reliability before Python analysis.

SELECT
    'Missing urgency level' AS issue,
    COUNT(*) AS affected_records
FROM service_requests
WHERE urgency_level IS NULL

UNION ALL

SELECT
    'Referrals without valid request',
    COUNT(*)
FROM referrals r
LEFT JOIN service_requests sr
    ON r.request_id = sr.request_id
WHERE sr.request_id IS NULL

UNION ALL

SELECT
    'Referrals without valid provider',
    COUNT(*)
FROM referrals r
LEFT JOIN providers p
    ON r.provider_id = p.provider_id
WHERE p.provider_id IS NULL

UNION ALL

SELECT
    'Referrals without outcome record',
    COUNT(*)
FROM referrals r
LEFT JOIN referral_outcomes ro
    ON r.referral_id = ro.referral_id
WHERE ro.referral_id IS NULL

UNION ALL

SELECT
    'Outcome records without referral',
    COUNT(*)
FROM referral_outcomes ro
LEFT JOIN referrals r
    ON ro.referral_id = r.referral_id
WHERE r.referral_id IS NULL;
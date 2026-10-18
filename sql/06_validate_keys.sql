-- 06: Validate Primary Keys
-- Checks total rows against unique IDs.
-- Identifies potential duplicate or missing IDs.

SELECT
    'service_requests' AS table_name,
    COUNT(*) AS total_rows,
    COUNT(DISTINCT request_id) AS unique_ids
FROM service_requests

UNION ALL

SELECT
    'referrals',
    COUNT(*),
    COUNT(DISTINCT referral_id)
FROM referrals

UNION ALL

SELECT
    'referral_outcomes',
    COUNT(*),
    COUNT(DISTINCT referral_id)
FROM referral_outcomes;
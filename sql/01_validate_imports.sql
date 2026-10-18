
-- Project: CommunityConnect Analytics
-- Purpose: Validate the number of records imported into each database table.

SELECT
    'Service Requests' AS table_name,
    COUNT(*) AS total_records
FROM service_requests

UNION ALL

SELECT 'Providers', COUNT(*)
FROM providers

UNION ALL

SELECT 'Referrals', COUNT(*)
FROM referrals

UNION ALL

SELECT 'Referral Outcomes', COUNT(*)
FROM referral_outcomes

UNION ALL

SELECT 'Data Quality Issues', COUNT(*)
FROM data_quality_issues;

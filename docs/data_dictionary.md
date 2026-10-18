
# CommunityConnect Analytics — Data Dictionary

## Project Purpose

Analyze fictional community service requests, referrals,
provider performance, and customer outcomes.

All operational records will be synthetic.

## 1. service_requests

One row represents one request for assistance.

| Field | Meaning |
|---|---|
| request_id | Unique identifier for each request |
| request_date | Date assistance was requested |
| service_category | Type of assistance requested |
| region | Fictional geographic service area |
| urgency_level | Low, Medium, or High |

## 2. providers

One row represents one service provider.

| Field | Meaning |
|---|---|
| provider_id | Unique provider identifier |
| provider_name | Fictional organization name |
| service_category | Type of assistance offered |
| region | Provider service area |
| capacity_status | Available, Limited, or Full |

## 3. referrals

One row represents one referral to a provider.

| Field | Meaning |
|---|---|
| referral_id | Unique referral identifier |
| request_id | Request associated with the referral |
| provider_id | Provider receiving the referral |
| referral_date | Date referral was made |

## 4. referral_outcomes

One row represents the latest recorded outcome for a referral.

| Field | Meaning |
|---|---|
| referral_id | Referral being tracked |
| outcome_status | Needs Met, Unsuccessful, Pending, Unknown |
| failure_reason | Documented reason if unsuccessful |
| follow_up_date | Date outcome was last checked |

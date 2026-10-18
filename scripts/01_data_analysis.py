import sqlite3
import pandas as pd

# Connect to our SQLite database
conn = sqlite3.connect("database/communityconnect.db")

# Load data into Pandas DataFrames
requests = pd.read_sql_query("SELECT * FROM service_requests", conn)
referrals = pd.read_sql_query("SELECT * FROM referrals", conn)
outcomes = pd.read_sql_query("SELECT * FROM referral_outcomes", conn)
providers = pd.read_sql_query("SELECT * FROM providers", conn)
quality_issues = pd.read_sql_query("SELECT * FROM data_quality_issues", conn)

conn.close()

# Verify data loaded successfully
print("Service Requests:", requests.shape)
print("Referrals:", referrals.shape)
print("Referral Outcomes:", outcomes.shape)
print("Providers:", providers.shape)
print("Data Quality Issues:", quality_issues.shape)

# Check missing values in all five datasets
for name, df in {
    "Service Requests": requests,
    "Referrals": referrals,
    "Referral Outcomes": outcomes,
    "Providers": providers,
    "Data Quality Issues": quality_issues
}.items():
    print(f"\n--- {name} ---")
    print("Missing values:")
    print(df.isnull().sum())
    print("\nData types:")
    print(df.dtypes)

# Examine documented data-quality problems
print("\n--- Documented Quality Issues ---")
print(quality_issues["issue_type"].value_counts())

# Step 3: Investigate missing values by outcome status
print("\n--- Missing Failure Reasons by Outcome ---")
print(
    outcomes.groupby("outcome_status")["failure_reason"]
    .apply(lambda x: x.isna().sum())
)

print("\n--- Missing Follow-up Dates by Outcome ---")
print(
    outcomes.groupby("outcome_status")["follow_up_date"]
    .apply(lambda x: x.isna().sum())
)

# Step 4: Validate referral and request dates
# Convert date strings into Python datetime values
# Identify referrals dated before their requests

requests["request_date"] = pd.to_datetime(
    requests["request_date"], errors="coerce"
)

referrals["referral_date"] = pd.to_datetime(
    referrals["referral_date"], errors="coerce"
)

# Match each referral to its original service request
date_check = referrals.merge(
    requests[["request_id", "request_date"]],
    on="request_id",
    how="left",
    validate="many_to_one"
)

# Identify referrals recorded before the request date
invalid_dates = date_check[
    date_check["referral_date"] < date_check["request_date"]
]

print("\n--- Date Validation ---")
print("Invalid request dates:", requests["request_date"].isna().sum())
print("Invalid referral dates:", referrals["referral_date"].isna().sum())
print("Referrals before requests:", len(invalid_dates))

print("\n--- Sample Date Issues ---")
print(
    invalid_dates[
        ["referral_id", "request_id", "request_date", "referral_date"]
    ].head()
)

# Step 5: Combine request, referral, outcome, and provider data
# Use shared IDs to connect related records
# Verify that the joins preserve all referral records

combined = referrals.merge(
    requests,
    on="request_id",
    how="left",
    validate="many_to_one"
)

combined = combined.merge(
    outcomes,
    on="referral_id",
    how="left",
    validate="one_to_one"
)

combined = combined.merge(
    providers,
    on="provider_id",
    how="left",
    suffixes=("_request", "_provider"),
    validate="many_to_one"
)

print("\n--- Combined Dataset ---")
print("Rows:", combined.shape[0])
print("Columns:", combined.shape[1])
print("Column names:", combined.columns.tolist())

# Step 5.1: Validate the combined dataset
# Check for missing information after joining tables
# Confirm every referral has related records

print("\n--- Join Validation ---")

print("Missing requests:",
      combined["request_date"].isna().sum())

print("Missing outcomes:",
      combined["outcome_status"].isna().sum())

print("Missing providers:",
      combined["provider_name"].isna().sum())

print("Duplicate referral IDs:",
      combined["referral_id"].duplicated().sum())

# Step 5.2: Flag data-quality issues
# Preserve all records in the combined dataset
# Mark referrals recorded before their request dates

combined["invalid_date_flag"] = (
    combined["referral_date"] < combined["request_date"]
)

combined["missing_urgency_flag"] = (
    combined["urgency_level"].isna()
)

print("\n--- Data Quality Flags ---")
print("Invalid referral dates:", combined["invalid_date_flag"].sum())
print("Missing urgency:", combined["missing_urgency_flag"].sum())
print("Total referrals:", len(combined))

# Step 5.3: Prepare referral-level data for Tableau
# Label missing urgency without inventing a value
# Export all referrals with their data-quality flags

combined["urgency_level"] = combined["urgency_level"].fillna("Unknown")

combined.to_csv(
    "data/processed/referral_analysis.csv",
    index=False
)

print("\n--- Export Complete ---")
print("File: data/processed/referral_analysis.csv")
print("Rows exported:", len(combined))
print("Missing urgency labels:",
      (combined["urgency_level"] == "Unknown").sum())


# Step 6: Summarize referrals at the request level
# Mark a request resolved if any referral has Needs Met
# Keep one row per original service request

request_summary = combined.groupby("request_id").agg(
    referral_count=("referral_id", "count"),
    has_success=("outcome_status", lambda x: (x == "Needs Met").any())
).reset_index()

request_analysis = requests.merge(
    request_summary,
    on="request_id",
    how="left",
    validate="one_to_one"
)

print("\n--- Request-Level Dataset ---")
print("Total requests:", len(request_analysis))
print("Requests with recorded success:", request_analysis["has_success"].sum())
print("Requests without recorded success:", (~request_analysis["has_success"]).sum())

# Step 6.1: Prepare request-level data for Tableau
# Label missing urgency and recorded resolution status
# Export one row per service request

request_analysis["urgency_level"] = (
    request_analysis["urgency_level"].fillna("Unknown")
)

request_analysis["resolution_status"] = (
    request_analysis["has_success"].map({
        True: "Needs Met",
        False: "No Recorded Success"
    })
)

request_analysis.to_csv(
    "data/processed/request_analysis.csv",
    index=False
)

print("\n--- Request Export Complete ---")
print("File: data/processed/request_analysis.csv")
print("Rows exported:", len(request_analysis))
print("\nResolution breakdown:")
print(request_analysis["resolution_status"].value_counts())


# Step 7: Validate final analysis datasets
# Check row counts, unique IDs, and key metrics
# Stop execution if any validation fails

assert len(combined) == 12500, "Referral count mismatch"
assert combined["referral_id"].is_unique, "Duplicate referral IDs"

assert len(request_analysis) == 10000, "Request count mismatch"
assert request_analysis["request_id"].is_unique, "Duplicate request IDs"

assert request_analysis["has_success"].sum() == 6386, "Success count mismatch"

assert combined["invalid_date_flag"].sum() == 35, "Date issue count mismatch"
assert combined["missing_urgency_flag"].sum() == 70, "Urgency issue count mismatch"

print("\n--- Final Validation ---")
print("All validation checks passed!")

from pathlib import Path
from contextlib import closing
import sqlite3
import pandas as pd


# Project paths and outcome definitions
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "database" / "communityconnect.db"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
SUCCESS_OUTCOME = "Needs Met"
UNKNOWN_URGENCY = "Unknown"


# Stop execution if an important data validation fails
def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    require(DATABASE_PATH.is_file(), f"Database not found: {DATABASE_PATH}")

    # Load the four related tables from SQLite
    with closing(sqlite3.connect(DATABASE_PATH)) as conn:
        requests = pd.read_sql_query("SELECT * FROM service_requests", conn)
        referrals = pd.read_sql_query("SELECT * FROM referrals", conn)
        outcomes = pd.read_sql_query("SELECT * FROM referral_outcomes", conn)
        providers = pd.read_sql_query("SELECT * FROM providers", conn)

    sources = {
        "Service Requests": requests,
        "Referrals": referrals,
        "Referral Outcomes": outcomes,
        "Providers": providers,
    }

    # Initial data profiling: record counts, missing values, and data types
    print("\n--- Source Data Profiling ---")

    for name, frame in sources.items():
        print(f"\n{name}: {len(frame):,} rows, {len(frame.columns)} columns")
        print("Missing values:\n", frame.isna().sum().to_string())
        print("Data types:\n", frame.dtypes.to_string())

    # Check missing fields by referral outcome to understand their context
    print("\n--- Missing Fields by Referral Outcome ---")

    for col in ["failure_reason", "follow_up_date"]:
        print(f"\nMissing {col}:")
        print(
            outcomes.groupby("outcome_status", dropna=False)[col]
            .apply(lambda series: series.isna().sum())
            .to_string()
        )

    # Check primary keys before joining tables to avoid duplicate records
    for frame, key, name in [
        (requests, "request_id", "service_requests"),
        (referrals, "referral_id", "referrals"),
        (outcomes, "referral_id", "referral_outcomes"),
        (providers, "provider_id", "providers"),
    ]:
        require(frame[key].notna().all(), f"Missing {key} in {name}")
        require(frame[key].is_unique, f"Duplicate {key} in {name}")

    # Convert dates for validation; invalid date formats become NaT
    requests["request_date"] = pd.to_datetime(
        requests["request_date"], errors="coerce"
    )
    referrals["referral_date"] = pd.to_datetime(
        referrals["referral_date"], errors="coerce"
    )

    # Join related tables while preserving all referrals
    combined = referrals.merge(
        requests,
        on="request_id",
        how="left",
        validate="many_to_one",
        indicator="_request_join"
    )

    missing_requests = (combined["_request_join"] != "both").sum()
    combined = combined.drop(columns="_request_join")

    combined = combined.merge(
        outcomes,
        on="referral_id",
        how="left",
        validate="one_to_one",
        indicator="_outcome_join"
    )

    missing_outcomes = (combined["_outcome_join"] != "both").sum()
    combined = combined.drop(columns="_outcome_join")

    combined = combined.merge(
        providers,
        on="provider_id",
        how="left",
        suffixes=("_request", "_provider"),
        validate="many_to_one",
        indicator="_provider_join"
    )

    missing_providers = (combined["_provider_join"] != "both").sum()
    combined = combined.drop(columns="_provider_join")

    # Verify that joins did not lose records or duplicate referrals
    print("\n--- Join Validation ---")
    print("Missing linked requests:", missing_requests)
    print("Missing linked outcomes:", missing_outcomes)
    print("Missing linked providers:", missing_providers)
    print("Duplicate referral IDs:", combined["referral_id"].duplicated().sum())

    require(
        not (missing_requests or missing_outcomes or missing_providers),
        "At least one referral is missing its related request, outcome, or provider"
    )
    require(len(combined) == len(referrals), "Joins changed the referral row count")
    require(combined["referral_id"].is_unique, "Joins duplicated referrals")

    # Flag data-quality issues without deleting or changing source records
    combined["invalid_date_flag"] = (
        combined["referral_date"] < combined["request_date"]
    )
    combined["missing_urgency_flag"] = combined["urgency_level"].isna()

    print("\n--- Independently Detected Data Quality Issues ---")
    print("Invalid request dates:", requests["request_date"].isna().sum())
    print("Invalid referral dates:", referrals["referral_date"].isna().sum())
    print("Referrals dated before requests:", combined["invalid_date_flag"].sum())
    print("Requests missing urgency:", requests["urgency_level"].isna().sum())
    print(
        "Referrals linked to missing-urgency requests:",
        combined["missing_urgency_flag"].sum()
    )

    print("Sample date issues:")
    print(
        combined.loc[
            combined["invalid_date_flag"],
            ["referral_id", "request_id", "request_date", "referral_date"]
        ].head()
    )

    # Summarize referrals by request to avoid counting requests multiple times
    # A request has recorded success if at least one referral is "Needs Met"
    request_summary = combined.groupby("request_id").agg(
        referral_count=("referral_id", "count"),
        has_success=(
            "outcome_status",
            lambda values: values.eq(SUCCESS_OUTCOME).any()
        ),
    ).reset_index()

    # Merge the summary back to retain all original service requests
    request_analysis = requests.merge(
        request_summary,
        on="request_id",
        how="left",
        validate="one_to_one"
    )

    request_analysis["referral_count"] = (
        request_analysis["referral_count"].fillna(0).astype(int)
    )

    request_analysis["has_success"] = (
        request_analysis["has_success"].fillna(False).astype(bool)
    )

    # Create readable outcome labels for Tableau reporting
    request_analysis["resolution_status"] = (
        request_analysis["has_success"].map({
            True: SUCCESS_OUTCOME,
            False: "No Recorded Success",
        })
    )

    # Keep missing urgency visible instead of assigning an assumed value
    combined["urgency_level"] = (
        combined["urgency_level"].fillna(UNKNOWN_URGENCY)
    )

    request_analysis["urgency_level"] = (
        request_analysis["urgency_level"].fillna(UNKNOWN_URGENCY)
    )

    # Reconcile calculated results against the original data
    require(
        len(request_analysis) == len(requests),
        "Request row count changed"
    )

    require(
        request_analysis["request_id"].is_unique,
        "Request IDs are not unique"
    )

    require(
        request_analysis["referral_count"].sum() == len(referrals),
        "Request referral counts do not reconcile to source referrals"
    )

    require(
        request_analysis["has_success"].sum()
        == combined.loc[
            combined["outcome_status"] == SUCCESS_OUTCOME,
            "request_id"
        ].nunique(),
        "Recorded successful request count does not reconcile"
    )

    require(
        len(request_analysis)
        == (
            request_analysis["has_success"].sum()
            + (~request_analysis["has_success"]).sum()
        ),
        "Request success categories do not partition all requests"
    )

    require(
        combined.loc[
            combined["missing_urgency_flag"], "urgency_level"
        ].eq(UNKNOWN_URGENCY).all(),
        "Some missing urgency values were not labeled correctly"
    )

    # Format dates consistently before exporting to Tableau
    for col in ["request_date", "referral_date"]:
        combined[col] = combined[col].dt.strftime("%Y-%m-%d")

    request_analysis["request_date"] = (
        request_analysis["request_date"].dt.strftime("%Y-%m-%d")
    )

    # Export separate request-level and referral-level datasets
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    referral_output = OUTPUT_DIR / "referral_analysis.csv"
    request_output = OUTPUT_DIR / "request_analysis.csv"

    combined.to_csv(referral_output, index=False)
    request_analysis.to_csv(request_output, index=False)

    # Display final metrics calculated directly from the processed data
    success_count = int(request_analysis["has_success"].sum())
    request_count = len(request_analysis)

    print("\n--- Final Validation ---")
    print(f"Total requests: {request_count:,}")
    print(f"Requests with recorded success: {success_count:,}")
    print(f"Requests without recorded success: {request_count - success_count:,}")

    print(
        f"Recorded request resolution rate: {success_count / request_count:.2%}"
        if request_count
        else "Recorded request resolution rate: n/a (no requests)"
    )

    print(f"Total referrals: {len(combined):,}")
    print(f"Saved: {request_output}")
    print(f"Saved: {referral_output}")
    print("All validation checks passed!")


if __name__ == "__main__":
    main()

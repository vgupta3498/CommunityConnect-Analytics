# CommunityConnect | Service Request & Referral Analytics

**SQL (SQLite) · Python · Tableau Public | End-to-End Data Analytics Portfolio Project**

### [Explore the Interactive Tableau Dashboard](https://public.tableau.com/app/profile/vikas.gupta7229/viz/CommunityConnectAnalyticsDashboard/Dashboard1)

## Project Overview

CommunityConnect is a portfolio analytics project examining how community-service requests move through referrals to recorded outcomes. Using **synthetic data**, the project combines SQL analysis, Python-based data preparation and validation, and an interactive Tableau dashboard to explore demand, regional variation, recorded resolution, and referral barriers.

**Scope:** 10,000 unique service requests, 12,500 referrals, and 120 providers. This is a demonstration project, not an evaluation of an actual service organization.

## Business Questions

1. How many service requests and referrals were recorded, and which services and regions account for the most demand?
2. What share of requests have at least one referral with a recorded **Needs Met** outcome?
3. How do recorded request-level resolution rates vary by service category and region?
4. What are the distributions of referral outcomes and recorded unsuccessful-referral reasons?
5. How do request volume and recorded resolution change over time?
6. What data-quality limitations should be considered when interpreting these measures?

## Key Performance Indicators

| Measure | Result |
| --- | ---: |
| Unique service requests | 10,000 |
| Referrals | 12,500 |
| Providers | 120 |
| Requests with at least one recorded **Needs Met** referral | 6,386 |
| Request-level recorded resolution rate | **63.86%** |
| Requests without a recorded **Needs Met** referral | 3,614 |

**Metric definition:** A request is counted as having recorded success if **at least one** associated referral is marked `Needs Met`. The request-level rate is `6,386 / 10,000 = 63.86%`. This is different from the referral-level percentage of `Needs Met` outcomes. Requests without recorded success are **not necessarily failures**; some referrals remain pending or have unknown outcomes.

## Key Findings

### 1. Recorded resolution differs across regions

| Region | Request-level recorded resolution rate |
| --- | ---: |
| West | 66.29% |
| Central | 65.39% |
| South | 64.75% |
| East | 62.19% |
| North | 60.68% |

The observed gap between West and North is **5.61 percentage points**. This identifies a useful area for follow-up investigation, not evidence that geography itself causes the difference.

### 2. Recorded resolution differs across service categories

| Service category | Request-level recorded resolution rate |
| --- | ---: |
| Healthcare | 66.20% |
| Food Assistance | 64.17% |
| Utility Assistance | 64.01% |
| Rental Assistance | 63.49% |
| Transportation | 62.39% |
| Employment Support | 62.03% |

Healthcare has the highest recorded rate and Employment Support the lowest, a **4.17-percentage-point** difference. Differences could reflect factors such as case mix, referral availability, or follow-up completeness; the analysis does not establish a cause.

### 3. Referral outcomes include substantial pending and unknown activity

| Referral outcome | Count | Share of referrals |
| --- | ---: | ---: |
| Needs Met | 7,222 | 57.8% |
| Unsuccessful | 2,370 | 19.0% |
| Pending | 1,794 | 14.4% |
| Unknown | 1,114 | 8.9% |
| **Total** | **12,500** | **100%** |

*Displayed percentages are rounded.* Pending and unknown referrals together account for **2,908 referrals (23.3% of all referrals)**. They should be kept distinct from recorded unsuccessful outcomes.

### 4. Recorded unsuccessful-referral reasons suggest operational questions

| Recorded reason | Referrals |
| --- | ---: |
| Ineligible | 591 |
| Unable to Contact | 537 |
| Provider At Capacity | 524 |
| Funding Unavailable | 488 |
| Other | 230 |
| **Total unsuccessful referrals** | **2,370** |

The most frequently recorded reasons are ineligibility, inability to contact, and provider capacity. Potential next questions include whether eligibility guidance, contact procedures, or provider-capacity information could be improved. These are **hypotheses for investigation**, not demonstrated interventions or causal findings.

## Interactive Dashboard

**[Open the CommunityConnect Tableau Dashboard →](https://public.tableau.com/app/profile/vikas.gupta7229/viz/CommunityConnectAnalyticsDashboard/Dashboard1)**

The dashboard brings together:

- KPI cards for total requests, recorded successes, and request-level resolution rate.
- Request volume by service category, region, and urgency level.
- Monthly request volume and recorded-resolution trends.
- Referral outcome distribution and unsuccessful-referral reasons.
- Resolution comparisons by service category and region, including a service-by-region heatmap.

The published Tableau Public visualization is the easiest way to explore the results. The Tableau workbook is also maintained in the project's `dashboards/` directory.

## Tools and Skills Demonstrated

| Tool | Application |
| --- | --- |
| **SQLite / SQL** | Relational analysis, joins, aggregation, request/referral outcome metrics, provider analysis, and data-quality checks |
| **Python** | Data analysis, validation, and preparation of request-level and referral-level CSV outputs |
| **Tableau Public** | Interactive KPI reporting, trend analysis, categorical comparisons, referral-outcome visualization, and heatmaps |
| **VS Code / GitHub** | Project organization, documentation, and version-controlled portfolio delivery |

## Analytics Workflow

1. **Source data:** Work with synthetic service-request, referral, referral-outcome, provider, and data-quality records.
2. **SQL exploration:** Analyze relationships and patterns across requests, referrals, outcomes, and providers. Validate keys and examine missing values.
3. **Python preparation:** Produce separate request-level and referral-level analytical datasets for visualization.
4. **Validation:** Check record counts and confirm request-level success logic before reporting metrics.
5. **Tableau visualization:** Build KPI cards, distribution charts, regional and service comparisons, a monthly trend, and a resolution heatmap.
6. **Publication:** Publish the interactive dashboard on Tableau Public and link it from this repository.

## Repository Structure

```text
CommunityConnect-Analytics/
├── dashboards/                # Tableau workbook(s)
├── data/
│   ├── raw/                   # Original synthetic data files (when included)
│   └── processed/             # Dashboard-ready analysis CSVs
│       ├── request_analysis.csv
│       └── referral_analysis.csv
├── database/                  # SQLite database files (when included)
├── docs/                      # Supporting notes/documentation
├── scripts/
│   └── 01_data_analysis.py    # Python analysis and export script
├── sql/                       # SQL analysis and validation queries
├── .gitignore
└── README.md
```

*Some generated data, local database files, or Tableau workbooks may be excluded from GitHub depending on repository size and `.gitignore` settings. The structure above describes the working project layout.*

## How to Explore or Reproduce the Analysis

### Option A: Explore the published results

Open the [interactive Tableau dashboard](https://public.tableau.com/app/profile/vikas.gupta7229/viz/CommunityConnectAnalyticsDashboard/Dashboard1). No local setup is required.

### Option B: Review the analysis locally

1. Clone or download this repository and open it in VS Code.
2. Review the SQL files in `sql/` to understand the analysis logic and data-quality checks.
3. Ensure the project's SQLite database and required input files are available at the locations referenced by the scripts. Local file paths may need adjustment.
4. Create a Python virtual environment and install the packages imported by `scripts/01_data_analysis.py` (the repository should document exact dependencies before claiming fully automated reproducibility).
5. From the project root, run:

   ```bash
   python scripts/01_data_analysis.py
   ```

6. Inspect `data/processed/request_analysis.csv` and `data/processed/referral_analysis.csv` and compare their row counts to the reported 10,000 requests and 12,500 referrals.
7. Open the workbook in `dashboards/` using Tableau Public, and reconnect its data sources to the local processed CSVs if prompted.

**Reproducibility note:** The analysis script may depend on a locally created SQLite database or raw files. The repository is fully reproducible only if those inputs, setup instructions, and exact Python dependencies are also included. The hosted Tableau dashboard remains accessible independently.

## Data Quality, Assumptions, and Limitations

- **Synthetic data:** All records are simulated. Findings illustrate an analytics workflow and must not be generalized to real communities or providers.
- **Unit of analysis:** Request-level resolution and referral-level outcomes use different denominators. A single request can have multiple referrals.
- **Recorded success:** A request is considered resolved for this analysis only when at least one associated referral is explicitly marked `Needs Met`.
- **Incomplete outcomes:** `Pending` and `Unknown` are not treated as unsuccessful. The 3,614 requests without recorded success must not be labeled confirmed failures.
- **Missing urgency:** The dataset includes **55 missing urgency-level values**; urgency-based visualizations should account for missingness.
- **Relational checks:** The project validation found no orphan keys in the checked relationships.
- **Interpretation:** Descriptive differences across regions or services do not demonstrate causation or measure program impact.

## Potential Next Steps

- Examine whether regional and service differences persist after accounting for urgency and referral volume.
- Investigate how pending and unknown outcomes affect reported success rates as follow-up data becomes available.
- Explore unsuccessful-referral patterns by provider capacity and service category.
- Add a pinned Python dependency file and database setup instructions for a fully reproducible GitHub workflow.

---

**Portfolio project:** CommunityConnect | Service Request & Referral Analytics  
**Dashboard:** [Tableau Public](https://public.tableau.com/app/profile/vikas.gupta7229/viz/CommunityConnectAnalyticsDashboard/Dashboard1)  
**Data:** Synthetic; for demonstration and learning purposes only.

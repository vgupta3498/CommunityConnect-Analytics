# CommunityConnect | Service Request & Referral Analytics

**SQL (SQLite) · Python (Pandas) · Tableau Public | Data Analytics Portfolio Project**

**[Explore the Interactive Tableau Dashboard](https://public.tableau.com/app/profile/vikas.gupta7229/viz/CommunityConnectAnalyticsDashboard/Dashboard1)**

## Project Overview

CommunityConnect is an end-to-end analytics project exploring how community-service requests move through referrals to recorded outcomes. Using **synthetic data**, the project combines SQL exploration, Python-based data preparation and validation, and an interactive Tableau dashboard to examine service demand, recorded resolution, regional differences, and barriers to successful referrals.

The dataset contains **10,000 unique service requests, 12,500 referrals, and 120 providers**. The analysis is a portfolio demonstration, **not an evaluation of a real community-service organization**. No actual client information is used.

The intended audience for this type of analysis would be service navigation managers, program leadership, reporting teams, and community partners who need to understand service demand and referral outcomes.

## Business Questions

1. Which service categories and regions have the highest request volumes?
2. What proportion of unique service requests have at least one referral recorded as `Needs Met`?
3. How does recorded request-level resolution vary by region and service category?
4. What are the distributions of referral outcomes and unsuccessful-referral reasons?
5. How do request volume and recorded resolution change over time?
6. What data-quality and outcome-reporting limitations affect the interpretation of these metrics?

## Data Sources

The analysis uses **four core synthetic CSV datasets** in `data/raw/`:

| File | Contents | Unit of analysis |
|---|---|---|
| `service_requests.csv` | Request ID, date, service category, region, and urgency | One row per request |
| `referrals.csv` | Referral ID, request ID, provider ID, and referral date | One row per referral |
| `referral_outcomes.csv` | Referral outcome, failure reason, and follow-up date | One recorded outcome per referral |
| `providers.csv` | Provider details, service category, region, and capacity status | One row per provider |

A single request can have **multiple referrals**, so request-level measures and referral-level measures must be calculated separately to avoid double-counting requests.

## Key Performance Indicators

| Measure | Result |
|---|---:|
| Unique service requests | 10,000 |
| Referrals | 12,500 |
| Providers | 120 |
| Requests with at least one `Needs Met` referral | 6,386 |
| **Request-level recorded resolution rate** | **63.86%** |
| Requests without recorded success | 3,614 |

**Metric definition:** A request has *recorded success* when **at least one** of its associated referrals has the outcome `Needs Met`.

**Recorded request resolution rate = 6,386 ÷ 10,000 = 63.86%.** This is not the same as the percentage of individual referrals marked `Needs Met`. A request without recorded success is **not necessarily a confirmed failure**; its referral outcomes may be pending, unknown, or unsuccessful.

## Key Findings

### 1. Recorded resolution varies by region

| Region | Request-level recorded resolution rate |
|---|---:|
| West | 66.29% |
| Central | 65.39% |
| South | 64.75% |
| East | 62.19% |
| North | 60.68% |

West has a recorded resolution rate **5.61 percentage points** higher than North. This difference identifies an area for further investigation; it does not prove that location causes the difference or that one regional team performs better.

### 2. Recorded resolution varies by service category

| Service category | Request-level recorded resolution rate |
|---|---:|
| Healthcare | 66.20% |
| Food Assistance | 64.17% |
| Utility Assistance | 64.01% |
| Rental Assistance | 63.49% |
| Transportation | 62.39% |
| Employment Support | 62.03% |

Healthcare has the highest recorded resolution rate, while Employment Support has the lowest, a **4.17-percentage-point difference**. Case mix, provider availability, and outcome-documentation practices would need further examination before drawing conclusions.

### 3. Rental and food assistance account for much of the demand

Rental Assistance accounts for **2,944 requests** and Food Assistance for **2,233 requests**. Together, these represent **5,177 requests (51.77%)**.

Central has the highest request volume (**2,083**), while West has **1,946**. Request volume provides context for comparing recorded outcomes and discussing resource needs.

### 4. Referral outcomes include pending and unknown records

| Referral outcome | Count | Share of referrals |
|---|---:|---:|
| Needs Met | 7,222 | 57.8% |
| Unsuccessful | 2,370 | 19.0% |
| Pending | 1,794 | 14.4% |
| Unknown | 1,114 | 8.9% |
| **Total** | **12,500** | **100%** |

*Individual percentages are rounded.*

The referral-level `Needs Met` share is **57.8%**, compared with the request-level recorded resolution rate of **63.86%**. These measures have different denominators and answer different questions.

Pending and Unknown account for **2,908 referrals (23.3%)** combined. Those records deserve closer review, but should **not** automatically be treated as unsuccessful or overdue.

### 5. Unsuccessful referrals show different types of barriers

| Recorded reason | Referrals |
|---|---:|
| Ineligible | 591 |
| Unable to Contact | 537 |
| Provider At Capacity | 524 |
| Funding Unavailable | 488 |
| Other | 230 |
| **Total unsuccessful referrals** | **2,370** |

The most frequent reasons are ineligibility, contact difficulties, and provider capacity. Possible follow-up questions include whether eligibility guidance, contact procedures, or provider-availability information could be improved. These are **hypotheses to investigate**, not proven causes or implemented changes.

## Data Quality and Validation

SQL and Python were used to inspect the source tables and check the integrity of the reporting outputs.

| Finding or check | Result | Treatment |
|---|---:|---|
| Requests with missing urgency | **55 unique requests** | Preserved; missing urgency labeled `Unknown` in reporting data |
| Referrals associated with those requests | **70 referral rows** | Flagged at the referral level |
| Referrals dated before their associated request | **35 referrals** | Flagged as `invalid_date_flag`; dates not silently corrected |
| Unmatched request, provider, or outcome records in referral joins | **0** | Join-integrity validation passed |
| Duplicate referral IDs after joining | **0** | Unique referral rows preserved |

**Why 55 and 70 are both correct:** Urgency belongs to a service request. The **55** figure counts unique requests missing urgency; those requests account for **70** rows in the referral-level data because some requests have more than one referral. These are not two separate sets of missing values.

The script also examines missing `failure_reason` and `follow_up_date` values by outcome status. Missing failure reasons should be interpreted in context: in this dataset, all referrals marked `Unsuccessful` have a recorded failure reason, while other statuses do not use that field in the same way.

The pipeline **flags** questionable records instead of inventing missing values or silently changing inconsistent dates. The date-ordering issues should be investigated before calculating referral turnaround times.

## Interactive Tableau Dashboard

**[Open the CommunityConnect Dashboard on Tableau Public →](https://public.tableau.com/app/profile/vikas.gupta7229/viz/CommunityConnectAnalyticsDashboard/Dashboard1)**

The dashboard includes:

- KPI cards for total requests, recorded successes, and request-level resolution rate.
- Request volume by service category, region, and urgency level.
- Monthly request-volume and recorded-resolution trends.
- Referral-outcome distribution and unsuccessful-referral reasons.
- Recorded resolution by service and region, including a service-by-region heatmap.

The Tableau workbook is stored in `dashboards/CommunityConnect Analytics Dashboard.twb`. The hosted Tableau Public version is the easiest way to view the finished analysis without local setup.

## Tools and Methods

| Tool | How it was used |
|---|---|
| **SQLite / SQL** | Import review, relational joins, key and relationship checks, aggregation, request-level outcome definitions, regional and provider analyses |
| **Python / Pandas** | Read SQLite tables, profile missing values, validate joins, detect date and urgency issues, build request/referral outputs, reconcile counts, export CSVs |
| **Tableau Public** | KPI reporting, demand and outcome charts, monthly trends, regional/service comparisons, and heatmap |
| **VS Code / GitHub** | Development, organization, documentation, and version control |

## Analytics Workflow

1. **Understand the source data:** Explore the four synthetic tables and their identifiers, including the one-to-many relationship between requests and referrals.
2. **Explore with SQL:** Check table counts, identifiers, missing values, relationships, referral outcomes, service demand, and regional patterns.
3. **Prepare with Python:** Join the four tables, validate cardinality, create data-quality flags, and generate separate request-level and referral-level analysis tables.
4. **Reconcile outputs:** Confirm that unique request counts, referral counts, and recorded-success calculations agree with the source data. Results are calculated from the records rather than asserted against fixed expected totals.
5. **Build the Tableau dashboard:** Visualize demand, recorded resolution, outcome distributions, referral barriers, and trends.
6. **Share and document:** Publish the interactive dashboard and maintain the project files in GitHub.

## Repository Structure

```text
CommunityConnect-Analytics/
├── dashboards/
│   └── CommunityConnect Analytics Dashboard.twb
├── data/
│   ├── raw/
│   │   ├── service_requests.csv
│   │   ├── referrals.csv
│   │   ├── referral_outcomes.csv
│   │   └── providers.csv
│   └── processed/
│       ├── request_analysis.csv
│       └── referral_analysis.csv
├── database/                    # Local SQLite database; ignored by Git
│   └── communityconnect.db
├── docs/
│   └── data_dictionary.md
├── scripts/
│   └── 01_data_analysis.py
├── sql/                         # SQL exploration and validation queries
├── .gitignore
└── README.md
```

`database/communityconnect.db` is a **local file**, not included in GitHub. The `.gitignore` also excludes `.venv/`, `.env`, temporary Tableau recovery files, and local DB Browser settings.

## How to Explore or Run the Project

### Option A — Explore the published dashboard

Open the **[interactive Tableau dashboard](https://public.tableau.com/app/profile/vikas.gupta7229/viz/CommunityConnectAnalyticsDashboard/Dashboard1)**. No Python, SQLite, or Tableau Desktop installation is needed to view it online.

### Option B — Run the analysis locally

1. Clone the repository:

   ```bash
   git clone https://github.com/vgupta3498/CommunityConnect-Analytics.git
   cd CommunityConnect-Analytics
   ```

2. Create a SQLite database at `database/communityconnect.db` and import the **four** CSV files from `data/raw/` as tables named:

   - `service_requests`
   - `referrals`
   - `referral_outcomes`
   - `providers`

   For example, you can use **DB Browser for SQLite** to create the database and import each CSV as a table, using the first CSV row as column headers. Save the database after importing. The project does not currently include an automated raw-CSV-to-SQLite import script.

3. Set up a Python environment and install Pandas:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install pandas
   ```

4. Run the preparation script from the project folder:

   ```bash
   python scripts/01_data_analysis.py
   ```

   The script validates source relationships, reports data-quality findings, calculates request-level success, and writes:

   - `data/processed/request_analysis.csv`
   - `data/processed/referral_analysis.csv`

5. To review the SQL logic, open the `.sql` files in `sql/` and run them against your SQLite database. To inspect the visualizations locally, open the Tableau workbook from `dashboards/` and reconnect it to the two processed CSV files if Tableau prompts for a data source location.

**Reproducibility note:** The Python preparation step is repeatable once the SQLite tables exist. Database creation and CSV import are still manual, and dependency versions are not yet pinned. The Tableau Public dashboard can be explored independently of those steps.

## Limitations and Interpretation

- **Synthetic data:** Results are illustrative, not evidence about actual communities, clients, providers, or program effectiveness.
- **Different units of analysis:** Request-level recorded resolution and referral-level `Needs Met` share use different denominators.
- **Recorded outcomes:** A request with no recorded `Needs Met` referral is not automatically a confirmed failure. Pending and Unknown referral outcomes remain separate.
- **Data quality:** Missing urgency and invalid date ordering are reported and flagged; the project does not invent replacements for them.
- **Descriptive analysis:** Differences across services, regions, or providers do not demonstrate causation. More operational context would be needed before acting on these patterns.
- **Outcome follow-up:** The available data does not establish whether every pending referral is overdue or whether every unknown outcome represents a documentation failure.

## Potential Improvements

- Automate database creation and CSV imports; add a pinned dependency file and repeatable setup checks.
- Investigate pending and unknown outcomes using reliable follow-up timelines.
- Analyze referral turnaround time after reviewing the invalid date records.
- Examine whether regional and service-category differences persist after considering urgency, service mix, and referral volume.
- Explore provider capacity and documented unsuccessful-referral reasons with operational teams before proposing interventions.

---

**Project:** CommunityConnect | Service Request & Referral Analytics  
**Live dashboard:** [Tableau Public](https://public.tableau.com/app/profile/vikas.gupta7229/viz/CommunityConnectAnalyticsDashboard/Dashboard1)  
**Code:** [GitHub repository](https://github.com/vgupta3498/CommunityConnect-Analytics)  
**Data:** Synthetic, for learning and portfolio demonstration

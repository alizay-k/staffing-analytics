# 🏢 Staffing Analytics — End-to-End Data Project

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=flat&logo=google-cloud&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat&logo=dbt&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=power-bi&logoColor=black)

> 🚧 Status: Complete

---

## 🎯 The Business Problem

A staffing agency sources candidates from 5 countries
but has no visibility into which are most efficient.
They assumed equal sourcing was optimal — the data
told a different story.

---

## 💡 The Key Finding

Pakistan fills roles 9.1 days faster than the overall average across 5 countries. Shifting 8% of sourcing volume toward Pakistan generates an estimated **$375,004 in annual savings**, calculated using a cost-per-day-unfilled methodology.

## 🏗 Project Architecture

Raw CSV (messy)
↓
Python cleaning pipeline
↓
Clean CSV → BigQuery upload
↓
dbt transformation (staging → intermediate → marts)
↓
Power BI dashboard

## 📊 Data Quality Issues Fixed

| Issue | Scale | Fix Applied |
|---|---|---|
| Missing placement fees | 394 rows (7.8%) | Median by job title group |
| Inconsistent country codes | 15 formats → 5 | Dictionary mapping |
| Inconsistent job titles | 16 formats → 4 | Dictionary mapping |
| Mixed date formats | 2 formats in same column | pd.to_datetime(dayfirst=True) |
| Duplicate rows | 23 rows | drop_duplicates() |

## 💰 ROI Analysis

Pakistan-based recruiters fill roles 9.1 days faster than the network average. Applying a cost-per-day-unfilled methodology to an 8% sourcing shift (a conservative, operationally realistic baseline that avoids straining recruiter capacity) produces an estimated annual saving of **$375,004**.

## 🔍 The 5-Question Framework

| Question | Answer |
|---|---|
| What was the business problem? | Agency had no visibility into sourcing efficiency |
| What was messy about the data? | 15 country formats, 16 title formats, 394 missing fees, mixed dates, 23 duplicates |
| What did I challenge? | The assumption that equal sourcing across all countries was optimal |
| What was the trade-off? | Recruiter retraining time against a $375,004 annual saving |
| What changed? | Recommended shift toward Pakistan sourcing, visualized in the final dashboard |

## 🗂 Project Structure

staffing-analytics/
├── data/
│ ├── raw/ ← messy CSVs (generated)
│ └── clean/ ← cleaned CSVs (pipeline output)
├── python/
│ ├── generate_data.py ← generates 5,023 messy rows
│ ├── cleaning_pipeline.py ← cleans all 5 quality issues
│ └── clean_clients_recruiters.py
├── sql/
│ ├── practice/ ← subqueries, CTEs, window functions
│ └── project/ ← 10 business analysis queries
├── dbt/staffing_dbt/
│ ├── models/staging/ ← stg_placements, stg_clients, stg_recruiters
│ ├── models/intermediate/ ← int_placements_joined
│ └── models/marts/ ← 5 rpt_ models
├── docs/
│ ├── data_audit_memo.md ← written before any cleaning
│ ├── data_dictionary.md ← every table and column documented
│ └── stakeholder_memo.md ← plain-language findings for VP
├── screenshots/ ← Power BI dashboard views
└── CHANGELOG.md


## 🚀 How to Run This Project

```bash
# Clone the repo
git clone https://github.com/alizay-k/staffing-analytics.git
cd staffing-analytics

# Install dependencies
pip install pandas numpy

# Generate messy data
python python/generate_data.py

# Run cleaning pipeline
python python/cleaning_pipeline.py

# Clean clients and recruiters
python python/clean_clients_recruiters.py
```

## 📸 Screenshots

See the `/screenshots` folder for the full 4-page Power BI dashboard, covering country efficiency, recruiter rankings, ROI breakdown, and monthly trends.

## 📬 Connect

- LinkedIn: [linkedin.com/in/alizay-kanwal](https://linkedin.com/in/alizay-kanwal)
- Email: alizaaykanwal@gmail.com

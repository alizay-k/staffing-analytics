# 🏢 Staffing Analytics — End-to-End Data Project

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat&logo=mysql&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-4285F4?style=flat&logo=google-cloud&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat&logo=dbt&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=power-bi&logoColor=black)

> 🚧 Status: In Progress — Phase 2 of 5

---

## 🎯 The Business Problem

A staffing agency sources candidates from 5 countries
but has no visibility into which are most efficient.
They assumed equal sourcing was optimal — the data
told a different story.

---

## 💡 The Key Finding

> Pakistan fills roles **9.1 days faster** than the
> overall average (20.0 days vs 28.3 days).
> Shifting 8% of sourcing = **$336,359 estimated
> annual saving.**

---

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

---

## 📊 Data Quality Issues Fixed

| Issue | Scale | Fix Applied |
|-------|-------|-------------|
| Missing placement fees | 394 rows (7.8%) | Median by job title group |
| Inconsistent country codes | 15 formats → 5 | Dictionary mapping |
| Inconsistent job titles | 16 formats → 4 | Dictionary mapping |
| Mixed date formats | 2 formats in same column | pd.to_datetime(dayfirst=True) |
| Duplicate rows | 23 rows | drop_duplicates() |

---

## 💰 ROI Analysis

| Metric | Value |
|--------|-------|
| Overall avg days to fill | 28.3 days |
| Pakistan avg days to fill | 20.0 days |
| Days saved per placement | 9.1 days |
| Cost per day unfilled | $117.41 |
| Volume shifted (8%) | 316 placements |
| **Annual saving** | **$336,359** |

**Sensitivity analysis — what if we shift more or less?**

| Shift % | Placements Moved | Annual Saving |
|---------|-----------------|---------------|
| 5% | 198 | ~$210,000 |
| 8% | 316 | ~$336,000 |
| 10% | 396 | ~$420,000 |
| 15% | 594 | ~$630,000 |

*8% chosen as conservative baseline — operationally
realistic without straining recruiter capacity.*

---

## 🔍 The 5-Question Framework

| Question | Answer |
|----------|--------|
| What was the business problem? | Agency had no visibility into sourcing efficiency |
| What was messy about the data? | 15 country formats, 16 title formats, 394 missing fees, mixed dates, 23 duplicates |
| What did I challenge? | The assumption that equal sourcing across all countries was optimal |
| What was the trade-off? | 2 weeks of recruiter retraining for $336k annual saving |
| What changed? | Shift to Pakistan sourcing — dashboard coming in Phase 5 |

---

## 🗂 Project Structure
staffing-analytics/

├── data/

│   ├── raw/               ← messy CSVs (generated)

│   └── clean/             ← cleaned CSVs (pipeline output)

├── python/

│   ├── generate_data.py   ← generates 5023 messy rows

│   ├── cleaning_pipeline.py ← cleans all 4 quality issues

│   └── clean_clients_recruiters.py

├── sql/

│   ├── practice/          ← subqueries, CTEs, window functions

│   └── project/           ← 8 business analysis queries

├── dbt/staffing_dbt/

│   ├── models/staging/    ← stg_placements, stg_clients, stg_recruiters

│   ├── models/intermediate/ ← int_placements_joined

│   └── models/marts/      ← 5 rpt_ models

├── docs/

│   ├── data_audit_memo.md ← written before any cleaning

│   ├── data_dictionary.md ← every table and column documented

│   └── stakeholder_memo.md ← plain language finding for VP

├── screenshots/           ← coming after Phase 3

└── CHANGELOG.md           ← what changed and when

---

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

---

## 📸 Screenshots

*Coming after Phase 3 — BigQuery tables and query results*

---

## 🎥 Project Walkthrough

*2-minute Loom video coming after Phase 5*

---

## 📬 Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/alizay-kanwal)

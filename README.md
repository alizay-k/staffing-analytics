# Staffing Analytics — End-to-End Data Project

**Status: In Progress — Week 1 Complete**

## The Business Problem
A staffing agency sources candidates from 5 countries 
but has no visibility into which countries are most 
efficient. Equal sourcing across all countries is 
assumed to be optimal — but is it?

## Key Finding
Pakistan fills roles 9.1 days faster than the overall 
average (20.0 days vs 28.3 days). Shifting 8% of 
non-Pakistan sourcing saves an estimated **$336,359 
annually**.

## The Challenge I Made
The agency assumed equal sourcing across countries 
was the right strategy. The data showed this assumption 
was costing them time and money.

## The Trade-off
Shifting sourcing requires retraining 5 recruiters — 
a 2-week disruption for an ongoing annual saving.

## Tech Stack
| Tool | Purpose |
|------|---------|
| Python + pandas | Data generation and cleaning |
| SQL | Business analysis queries |
| Google BigQuery | Cloud data warehouse |
| dbt | Data transformation and testing |
| Power BI | Dashboard and visualization |

## Project Structure
- `data/raw/` — original messy CSV files
- `data/clean/` — cleaned files ready for BigQuery
- `python/` — generation and cleaning scripts
- `sql/` — practice queries and project queries
- `dbt/` — transformation models and tests
- `docs/` — data dictionary, audit memo, stakeholder memo
- `screenshots/` — portfolio evidence

## Data Quality Issues Found and Fixed
| Issue | Scale | Fix |
|-------|-------|-----|
| Missing placement fees | 394 rows (7.8%) | Filled with median by job title |
| Inconsistent country codes | 15 formats → 5 | Mapped to full country name |
| Inconsistent job titles | 16 formats → 4 | Standardized mapping dictionary |
| Mixed date formats | DD/MM/YYYY + YYYY-MM-DD | pd.to_datetime(dayfirst=True) |
| Duplicate rows | 23 rows | drop_duplicates() |

## ROI Analysis
| Metric | Value |
|--------|-------|
| Overall avg days to fill | 28.3 days |
| Pakistan avg days to fill | 20.0 days |
| Days saved per placement | 9.1 days |
| Cost per day unfilled | $117.41 |
| Placements shifted (8%) | 316 |
| **Estimated annual saving** | **$336,359** |

*Dashboard, Loom walkthrough, and BigQuery screenshots 
coming after Phase 3*
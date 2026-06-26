# Data Audit Memo
**Date:** June 22, 2026
**Dataset:** placements_messy.csv
**Written:** Before any cleaning code was written
**Total rows:** 5023

## Issues Found Before Cleaning

| Issue | Detail | Scale |
|-------|--------|-------|
| Missing fees | placement_fee column | 394 rows (7.8%) |
| Country formats | pak, PK, Pakistan all in same column | 15 formats for 5 countries |
| Job title formats | Sr. IT vs Senior IT vs Senior IT Support | 16 formats for 4 roles |
| Date formats | DD/MM/YYYY and YYYY-MM-DD mixed | Both formats in same column |
| Duplicate rows | Exact duplicate rows | 23 rows |

## Cleaning Plan and Order

1. **Dates first** — fill_date and job_post_date needed 
   for days_to_fill verification. Can't verify calculations 
   on inconsistent date strings.

2. **Country codes second** — ROI analysis groups by country. 
   pak, PK, Pakistan would be counted as 3 separate countries 
   breaking the groupby entirely.

3. **Job titles third** — fee imputation groups by job title. 
   Need clean titles before filling missing fees or the 
   median would be calculated on too-small groups.

4. **Missing fees fourth** — depends on clean job titles 
   from step 3. Fill with median by job title, not overall 
   median, because Senior roles have very different fee 
   ranges than Junior roles.

5. **Duplicates last** — remove after all standardization 
   so we catch duplicates that were previously hidden by 
   inconsistent formatting.

## What I Did Not Fix
- `client_id` and `recruiter_id` — both clean, no action needed
- `days_to_fill` — verified against date arithmetic rather 
  than independently fixed. If dates are clean and days 
  don't match, that would indicate a data pipeline problem 
  worth flagging to the data owner.

## Questions I Would Ask the Data Owner
1. Why are country codes inconsistent — are two separate 
   systems feeding this column?
2. Are the 23 duplicates from a CSV being exported twice, 
   or a system error?
3. Is 7.8% missing fees normal — or does it indicate a 
   process problem with fee recording?
4. Should missing fees be treated as deals that fell 
   through (true zero) rather than unknown values?

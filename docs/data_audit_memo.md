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
*Note: Order was updated during self-review. 
Original order had duplicates last — changed to 
duplicates before fee imputation after identifying 
that duplicate rows could skew median calculation.*

1. **Dates first** — fill_date and job_post_date needed 
   for days_to_fill verification. Can't verify calculations 
   on inconsistent date strings.

2. **Country codes second** — ROI analysis groups by country. 
   pak, PK, Pakistan would be counted as 3 separate countries 
   breaking the groupby entirely.

3. **Job titles third** — fee imputation groups by job title. 
   Need clean titles before filling missing fees or the 
   median would be calculated on too-small groups.

4. **Duplicates fourth** — remove BEFORE filling missing 
   fees. Reason: duplicate rows could skew the median 
   calculation used for fee imputation. Even for exact 
   duplicates, deduplicating first is the safer 
   professional practice — in real data, near-duplicates 
   (same placement recorded twice with slightly different 
   values) would inflate or deflate the median if not 
   removed first. Caught and fixed during self-review.

5. **Missing fees fifth** — filled AFTER deduplication 
   so median is calculated on unique records only. 
   Used median by job title group, not overall median, 
   because Senior roles ($3,000-$8,000) have very 
   different fee ranges than Junior roles ($1,000-$4,000). 
   Using overall median would under-impute Senior fees 
   and over-impute Junior fees.
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

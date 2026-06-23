# Data Dictionary

## Table: placements (fact table)
*Primary analytical table — one row per placement*

| Column | Type | Description | Cleaning Notes |
|--------|------|-------------|----------------|
| placement_id | INTEGER | Unique placement identifier | Primary key — verified unique |
| job_title | STRING | Role being filled | Standardized from 16 formats to 4 clean titles |
| job_post_date | DATE | Date role was posted | Standardized from mixed DD/MM/YYYY and YYYY-MM-DD |
| fill_date | DATE | Date role was filled | Standardized — verified against days_to_fill |
| days_to_fill | INTEGER | Days between post and fill date | Verified: (fill_date - job_post_date) = days_to_fill |
| placement_fee | NUMERIC | Revenue earned from placement | 394 nulls filled with median fee by job_title group |
| client_id | INTEGER | Foreign key → clients table | Clean — no issues found |
| recruiter_id | INTEGER | Foreign key → recruiters table | Clean — no issues found |
| candidate_country | STRING | Country candidate was sourced from | Standardized from 15 formats to 5 clean country names |
| client_country | STRING | Country client is based in | Clean — no issues found |

## Table: clients (dimension table)
*Lookup table — one row per client company*

| Column | Type | Description | Cleaning Notes |
|--------|------|-------------|----------------|
| client_id | INTEGER | Unique client identifier | Primary key — verified unique |
| client_name | STRING | Client company name | Whitespace stripped |
| industry | STRING | Client industry sector | Whitespace stripped |
| client_country | STRING | Country client is based in | Whitespace stripped |
| contract_start | DATE | Date contract began | Converted to datetime |
| monthly_retainer | NUMERIC | Monthly fee paid by client | Clean — no issues found |

## Table: recruiters (dimension table)
*Lookup table — one row per recruiter*

| Column | Type | Description | Cleaning Notes |
|--------|------|-------------|----------------|
| recruiter_id | INTEGER | Unique recruiter identifier | Primary key — verified unique |
| recruiter_name | STRING | Recruiter full name | Whitespace stripped |
| seniority | STRING | Junior / Mid / Senior | Whitespace stripped |
| base_country | STRING | Country recruiter works from | Whitespace stripped |
| hire_date | DATE | Date recruiter joined agency | Converted to datetime |
| target_placements_monthly | INTEGER | Monthly placement target | Clean — no issues found |

## Relationships
```
placements.client_id → clients.client_id
placements.recruiter_id → recruiters.recruiter_id
```
# Changelog

## [Week 1] — June 22-27, 2026

### Added
- `generate_data.py` — generates 5023 rows of realistic 
  messy staffing data with 4 intentional quality issues
- `cleaning_pipeline.py` — full cleaning pipeline with 
  documented before/after counts for every issue
- `clean_clients_recruiters.py` — light cleaning for 
  clients and recruiters lookup tables
- `data_audit_memo.md` — written before any cleaning began
- `data_dictionary.md` — every table and column documented
- `stakeholder_memo.md` — plain language finding for VP
- `README.md` — business problem, findings, ROI, tech stack

### Data Quality Issues Fixed
- 394 missing fees → filled with median by job title
- 15 country formats → standardized to 5 clean names
- 16 job title formats → standardized to 4 clean titles
- 23 duplicate rows → removed with drop_duplicates()
- Mixed date formats → standardized to YYYY-MM-DD

### Key Finding
Pakistan fills roles 9.1 days faster than average.
Shifting 8% of non-Pakistan sourcing → $336,359 
estimated annual saving.

## [June 27, 2026]

### SQL Practice Progress
- Completed SQL Sections 1-6 on CSV Fiddle
- Sections 1-4: SELECT, WHERE, ORDER BY, 
  GROUP BY, aggregations — minimal mistakes
- Section 5: HAVING vs WHERE — understood
  the difference between filtering rows (WHERE)
  and filtering groups (HAVING)
- Section 6: JOINs — in progress
- Practice files added to sql/practice/

### Note on commit gap (June 24-27)
- SQL practice done on CSV Fiddle externally
- Code now committed retroactively
- Going forward: commit daily regardless
  of where practice happens
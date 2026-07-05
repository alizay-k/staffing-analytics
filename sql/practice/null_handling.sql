-- SECTION 9: NULL Handling Practice
-- Completed: June 28, 2026
-- Platform: CSV Fiddle
-- Dataset: placements_messy.csv and placements_clean.csv

-- Q1: Count missing fees in messy dataset
select count(*) as placement_fee from placements_messy where placement_fee is null

-- Q2: Replace NULL fees with 0 using COALESCE
select coalesce(placement_fee,0) from placements_clean

-- Q3: Replace NULL fees with text 'Missing'
select coalesce(cast(placement_fee as varchar),'Missing') from placements_clean

-- Q4: Compare AVG with and without NULL replacement
select avg(placement_fee) as avg_ignoring_nulls,
       avg(coalesce(placement_fee,0)) as avg_replacing_null_with_0
       from placements_clean

-- Q5: Find rows where fee is NULL OR fill time is high
select placement_fee,days_to_fill from placements_clean 
where placement_fee is null or days_to_fill >40
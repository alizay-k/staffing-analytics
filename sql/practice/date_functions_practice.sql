-- SECTION 8: Date Functions Practice
-- Completed: June 27, 2026
-- Platform: CSV Fiddle
-- Dataset: placements_clean.csv

-- Q1: Extract year from job_post_date
select strftime('%Y',job_post_date) as year from placements_clean

-- Q2: Extract month from job_post_date
select strftime('%m',job_post_date) as month from placements_clean

-- Q3: Count placements per month (year-month format)
select count(placement_id) as placement_count,strftime('%Y-%m',job_post_date) as month 
from placements_clean group by month 

-- Q4: Count placements per year
select count(placement_id) as placement_count,strftime('%Y',job_post_date) as year
from placements_clean group by year 

-- Q5: All placements from 2023 only
select placement_id,strftime('%Y',job_post_date) as year
from placements_clean where strftime('%Y',job_post_date)='2023'

-- Q6: Placements in first half of 2024
SELECT placement_id, job_post_date
FROM placements_clean
WHERE job_post_date >= '2024-01-01'
  AND job_post_date < '2024-07-01';

-- Q7: Verify days_to_fill matches date difference
SELECT 
    placement_id,
    job_post_date,
    fill_date,
    days_to_fill,
    JULIANDAY(fill_date) - JULIANDAY(job_post_date) AS calculated_days,
    CASE 
        WHEN days_to_fill = JULIANDAY(fill_date) - JULIANDAY(job_post_date) 
        THEN 'MATCH' 
        ELSE 'MISMATCH' 
    END AS verification_status
FROM placements_clean
WHERE job_post_date IS NOT NULL 
  AND fill_date IS NOT NULL
LIMIT 10;

-- Q8: Placements per month ordered chronologically
select count(placement_id) as placement_count,strftime('%Y-%m',job_post_date) as month 
from placements_clean group by month order by month desc

-- Q9: Month with highest total placement fee
select sum(placement_fee) as total_fee,strftime('%Y-%m',job_post_date) as month
from placements_clean group by month order by total_fee desc

-- Q10: Placements filled within 20 days
SELECT
    strftime('%Y-%m', job_post_date) AS month,
    AVG(placement_fee) AS avg_fee
FROM placements_clean
GROUP BY month
ORDER BY avg_fee DESC
LIMIT 1;





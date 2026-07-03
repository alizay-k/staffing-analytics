-- SECTION 7: CASE WHEN Practice Queries
-- Completed: July 3, 2026
-- Platform: CSV Fiddle
-- Dataset: placements_clean.csv


-- Q1: Speed category per placement
select days_to_fill,
case when days_to_fill < 22 then 'Fast'
when days_to_fill between 22 and 30 then 'Average'
else 'Slow'
end as speed_category
from placements_clean 

-- Q2: Fee tier per placement
select placement_fee,
case when placement_fee < 2000 then 'Low'
when placement_fee between 2000 and 5000 then 'Medium'
else 'High'
end as fee_tier
from placements_clean 

-- Q3: Count placements per speed category
select 
case
when days_to_fill < 22 then 'Fast'
when days_to_fill between 22 and 30 then 'Average'
else 'Slow'
end as speed_category,
count(*) as placement_count
from placements_clean 
group by speed_category

-- Q4: Total fees for fast vs slow placements
SELECT 
    CASE 
        WHEN days_to_fill < 22 THEN 'Fast'
        ELSE 'Slow'
    END AS speed_category,
    sum(placement_fee) as total_placement
FROM placements_clean
GROUP BY speed_category;

-- Q5: ROI flag + speed category combined (your query)
SELECT
    CASE
        WHEN days_to_fill < 22 THEN 'Fast'
        WHEN days_to_fill BETWEEN 22 AND 30 THEN 'Average'
        WHEN days_to_fill > 30 THEN 'Slow'
    END AS speed_category,
    CASE
        WHEN candidate_country IN ('Pakistan', 'India')
            THEN 'Positive ROI'
        WHEN candidate_country IN ('Nigeria', 'Kenya')
            THEN 'Negative ROI'
        WHEN candidate_country = 'Philippines'
            THEN 'Neutral'
        ELSE 'Unknown'
    END AS roi_flag,
    COUNT(placement_id) AS placement_count,
    SUM(placement_fee) AS total_fees,
    AVG(days_to_fill) AS avg_days
FROM placements_clean
GROUP BY speed_category, roi_flag
ORDER BY speed_category, total_fees DESC;
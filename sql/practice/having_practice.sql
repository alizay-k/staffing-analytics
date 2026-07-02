-- ─────────────────────────────────────────────────────
-- SECTION 5: HAVING Practice Queries
-- Completed: June 27, 2026
-- Platform: CSV Fiddle
-- Dataset: placements_clean.csv
-- 
-- Key concept: HAVING filters GROUPS after aggregation

-- Q46: Job titles with above-average fees

SELECT 
    job_title,
    AVG(placement_fee) AS avg_fee
FROM placements_clean
GROUP BY job_title
HAVING avg_fee > 4000;


-- Q47: Countries generating over $1M total revenue


SELECT 
    candidate_country,
    SUM(placement_fee) AS total_fee
FROM placements_clean
GROUP BY candidate_country
HAVING total_fee > 1000000;



-- Q48: High volume recruiters (200+ placements)


SELECT 
    recruiter_id,
    COUNT(placement_id) AS total_placements
FROM placements_clean
GROUP BY recruiter_id
HAVING total_placements > 200;



-- Q50: High volume AND high value job titles

SELECT 
    job_title,
    COUNT(placement_id) AS total_placements,
    AVG(placement_fee) AS avg_fee
FROM placements_clean
GROUP BY job_title
HAVING total_placements > 300 
   AND avg_fee > 3500;
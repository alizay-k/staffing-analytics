-- ─────────────────────────────────────────
-- SECTION 1-4: Basic SQL Practice
-- Completed: June 27, 2026
-- Platform: CSV Fiddle
-- Dataset: placements_clean.csv
-- ─────────────────────────────────────────

-- Q1: Select all columns, limit 10 rows
SELECT * FROM placements LIMIT 10;

-- Q2: Select specific columns
SELECT placement_id, candidate_country, 
       days_to_fill, placement_fee
FROM placements;

-- Q3: Count total placements
SELECT COUNT(*) AS total_placements 
FROM placements;

-- Q4: Average days to fill
SELECT AVG(days_to_fill) AS avg_days 
FROM placements;

-- Q5: Total revenue
SELECT SUM(placement_fee) AS total_revenue 
FROM placements;

-- Q6: Placements per country
SELECT candidate_country, 
       COUNT(*) AS placements
FROM placements
GROUP BY candidate_country
ORDER BY placements DESC;

-- Q7: Average days per country fastest first
SELECT candidate_country,
       AVG(days_to_fill) AS avg_days
FROM placements
GROUP BY candidate_country
ORDER BY avg_days ASC;

-- Q8: Filter Pakistan only
SELECT * FROM placements
WHERE candidate_country = 'Pakistan';

-- Q9: Filter high value placements
SELECT * FROM placements
WHERE placement_fee > 5000;

-- Q10: Top 5 highest fees
SELECT placement_id, placement_fee,
       candidate_country
FROM placements
ORDER BY placement_fee DESC
LIMIT 5;
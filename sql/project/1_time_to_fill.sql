-- Query 1: Time To Fill Analysis
-- Business question: Which job titles take longest
--                    to fill and are they worth the wait?
-- Why it matters: Slow roles cost more per placement.
--                 Identifies where to focus recruiter
--                 training or adjust client expectations.
-- Concepts: GROUP BY, AVG, SUM, COUNT, ORDER BY

select job_title,
round(avg(placement_fee),0) as avg_fee,
round(sum(placement_fee),0) as total_revenue,
avg(days_to_fill) as avg_days,
count(*) as no_of_placements
from placements_clean group by job_title order by avg_days desc
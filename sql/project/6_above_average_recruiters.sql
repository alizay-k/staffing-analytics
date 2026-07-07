-- Query 6: Above Average Recruiters
-- Business question: Which recruiters outperform the
--                    company revenue average?
-- Why it matters: Identifies star performers without
--                 manually comparing every recruiter.
--                 The difference column shows by how
--                 much each recruiter exceeds average.
-- Concepts: CTE, subquery in WHERE, subquery in SELECT

with recruiter_summary as (
select recruiter_id,
      round(sum(placement_fee),0)as total_fee,
      count(*) as no_of_placements
      from placements_clean
      group by recruiter_id)
       
select recruiter_id,total_fee - (select avg(total_fee) from recruiter_summary) as above_average 
from recruiter_summary 
WHERE total_fee > (SELECT AVG(total_fee) FROM recruiter_summary)
order by above_average desc

-- Query 3: Recruiter Revenue Ranking
-- Business question: How do recruiters rank by total
--                    revenue generated?
-- Why it matters: Identifies top performers for
--                 recognition and bottom performers
--                 for coaching. Links to $31k recruiter
--                 performance gap ROI finding.
-- Concepts: CTE, RANK() OVER (ORDER BY DESC)

with recruiter_ranking as (select recruiter_id,
round(sum(placement_fee),0)as total_revenue,
count(*) as no_of_placements
from placements_clean 
group by recruiter_id)

select recruiter_id,total_revenue,rank () over (order by total_revenue desc) as recruiter_rank 
from recruiter_ranking 
order by recruiter_rank
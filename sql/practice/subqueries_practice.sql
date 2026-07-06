
-- Subquery Practice Queries
-- Completed: July 6, 2026


-- 1. Countries with average days to fill less than 25
select * from (
    select candidate_country, avg(days_to_fill) as avg_days 
    from placements_clean 
    group by candidate_country 
) as avg_summary 
where avg_days < 25;

-- 2. Recruiters with total revenue greater than 500,000
select * from (
    select recruiter_id, sum(placement_fee) as total_revenue 
    from placements_clean 
    group by recruiter_id 
) as total_revenue_per_recruiter 
where total_revenue > 500000;

-- 3. Average placement_fee per candidate_country (above $3,800)
select candidate_country, avg_fee 
from (
    select candidate_country, avg(placement_fee) as avg_fee 
    from placements_clean 
    group by candidate_country
) as avg_p_country 
where avg_fee > 3800;

-- 4. Total placements per recruiter_id (more than 150 placements)
select recruiter_id, no_of_placements 
from (
    select recruiter_id, count(placement_id) as no_of_placements 
    from placements_clean 
    group by recruiter_id
) as placements_per_recruiter 
where no_of_placements > 150;
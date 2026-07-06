-- Window Functions Practice Queries
-- Completed: July 6, 2026

-- 1. Rank all placements by placement_fee (highest gets rank 1)
select placement_id, candidate_country, placement_fee, 
       rank() over (order by placement_fee desc) as fee_rank 
from placements_clean;

-- 2. For each country, rank recruiters by total fees (show only rank 1)
with recruiter_fees as (
    select recruiter_id, candidate_country, sum(placement_fee) as total_fee
    from placements_clean
    group by recruiter_id, candidate_country
),
ranked as (
    select recruiter_id, candidate_country, total_fee,
           rank() over (partition by candidate_country order by total_fee desc) as rank_country
    from recruiter_fees
)
select *
from ranked
where rank_country = 1
order by candidate_country;

-- 3. Monthly placement count with previous month's count and difference
with monthly_count as (
    select strftime('%Y-%m', job_post_date) as month,
           count(placement_id) as no_placement 
    from placements_clean
    group by month
)
select month, no_placement,
       lag(no_placement) over(order by month) as prev_month,
       no_placement - lag(no_placement) over(order by month) as diff_per_month
from monthly_count
order by month;

-- 4. Each placement's fee, running total ordered by job_post_date, 
-- and rank by fee within job_title
with fee_total as (
    select placement_fee, job_title, job_post_date 
    from placements_clean
)
select placement_fee, job_post_date, job_title, 
       sum(placement_fee) over (order by job_post_date) as running_total,
       rank() over(partition by job_title order by placement_fee desc) as fee_rank
from fee_total
order by job_post_date;
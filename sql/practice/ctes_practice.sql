-- Ctes Practice Queries
-- Completed: July 6, 2026



-- 1. Countries with average days to fill less than 25
with avg_summary as (
    select candidate_country, avg(days_to_fill) as avg_days 
    from placements_clean 
    group by candidate_country
)
select * from avg_summary where avg_days < 25;

-- 2. Recruiters with total revenue greater than 500,000
with total_revenue_per_recruiter as (
    select recruiter_id, sum(placement_fee) as total_revenue 
    from placements_clean 
    group by recruiter_id
)
select * from total_revenue_per_recruiter where total_revenue > 500000;

-- 3. Compare Pakistan average days vs overall average
with pakistan_avg as (
    select avg(days_to_fill) as pak_avg 
    from placements_clean 
    where candidate_country = 'Pakistan'
),
whole_avg as (
    select avg(days_to_fill) as overall_avg 
    from placements_clean
)
select pak_avg, overall_avg from pakistan_avg, whole_avg;

-- 4. Monthly placement counts
with total_count as (
    select extract(month from job_post_date) as month, 
           count(*) as total_placement 
    from placements_clean 
    group by extract(month from job_post_date)
)
select * from total_count order by total_placement desc;

-- 5. Average fee per job title with original data
with avg_per_job_title as (
    select job_title, avg(placement_fee) as avg_fee 
    from placements_clean 
    group by job_title
)
select p.job_title, a.avg_fee 
from placements_clean p 
join avg_per_job_title a on p.job_title = a.job_title;

-- 6. Average placement_fee per candidate_country (above $3,800)
with avg_p_country as (
    select candidate_country, avg(placement_fee) as avg_fee 
    from placements_clean 
    group by candidate_country
)
select candidate_country, avg_fee from avg_p_country where avg_fee > 3800;

-- 7. Total placements per recruiter_id (more than 150 placements)
with placements_per_recruiter as (
    select recruiter_id, count(placement_id) as no_of_placements 
    from placements_clean 
    group by recruiter_id
)
select recruiter_id, no_of_placements 
from placements_per_recruiter 
where no_of_placements > 150;

-- 8. Compare Pakistan and Nigeria average days
with pak_avg as (
    select candidate_country, avg(days_to_fill) as avg_pak 
    from placements_clean
    group by candidate_country 
    having candidate_country = 'Pakistan'
),
nigeria_avg as (
    select candidate_country, avg(days_to_fill) as avg_nig 
    from placements_clean
    group by candidate_country 
    having candidate_country = 'Nigeria'
)
select avg_pak, avg_nig, (avg_pak - avg_nig) as difference 
from pak_avg, nigeria_avg;

-- 9. Each placement with its country's average days (above/below comparison)
with avg_country as (
    select candidate_country, avg(days_to_fill) as avg_days 
    from placements_clean 
    group by candidate_country
)
select p.placement_id, p.candidate_country, p.days_to_fill, a.avg_days,
       case 
           when p.days_to_fill < a.avg_days then 'Below'
           when p.days_to_fill > a.avg_days then 'Above'
           else 'Average'
       end as below_above_avg 
from placements_clean p 
join avg_country a on p.candidate_country = a.candidate_country;

-- 10. Monthly placement count with previous month comparison
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

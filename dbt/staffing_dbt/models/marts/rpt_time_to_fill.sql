with placements as (
    select 
          placement_id,
          job_title,
          placement_fee_imputed,
          days_to_fill
    from {{ref('int_fees_imputed')}}
)

select 
      job_title,
      count(placement_id) as placement_count,
      round(sum(placement_fee_imputed),0) as total_revenue,
      round(avg(placement_fee_imputed),0) as avg_fee,
      round(avg(days_to_fill),1) as avg_days_to_fill
from placements
group by job_title
order by avg_days_to_fill desc
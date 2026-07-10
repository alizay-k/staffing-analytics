with placements as(
    select 
          recruiter_id,
          placement_id,
          placement_fee_imputed
    from {{ref('int_fees_imputed')}}
),

recruiter_ranking as (
    select 
          recruiter_id,
          round(sum(placement_fee_imputed),0) as total_fee,
          round(avg(placement_fee_imputed),0) as avg_fee,
          count(placement_id) as placement_count
    from placements 
    group by recruiter_id
)

select 
      recruiter_id,
      placement_count,
      total_fee,
      avg_fee,
      rank() over (order by total_fee desc) as revenue_rank
from recruiter_ranking
order by revenue_rank

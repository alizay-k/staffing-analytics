with placements as (
    select 
          placement_id,
          days_to_fill,
          candidate_country,
          placement_fee_imputed

    from {{ref('int_fees_imputed')}}
),

country_stats as (
    select
         candidate_country,
         count(placement_id) as placement_count,
         round(avg(days_to_fill),1) as avg_days,
         round(sum(placement_fee_imputed),0) as total_fee,
         round(avg(placement_fee_imputed),0) as avg_fee
         from placements
         group by candidate_country
)

select
      candidate_country,
      placement_count,
      avg_days,
      total_fee,
      avg_fee,
      round(avg_days -(select avg(days_to_fill) from {{ref('int_fees_imputed')}}),1)
      as days_vs_overall_avg 
from country_stats
order by avg_days asc
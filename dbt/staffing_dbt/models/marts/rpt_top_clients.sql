with placements as (
    select
          placement_id, 
          client_name,
          industry,
          placement_fee_imputed
    from {{ref('int_fees_imputed')}}      
)

select 
    client_name,
    count(placement_id) as placement_count,
    round(avg(placement_fee_imputed),0) as avg_fee,
    round(sum(placement_fee_imputed),0) as total_revenue
from placements
group by client_name,industry
order by total_revenue desc
limit 20


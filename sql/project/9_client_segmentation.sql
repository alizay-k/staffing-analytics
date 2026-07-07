-- Query 9: Client Value Segmentation
-- Business question: How are clients distributed across
--                    High, Medium, and Low value tiers?
-- Why it matters: Enables tiered service strategy.
--                 High-tier clients get dedicated
--                 account managers. Low-tier clients
--                 may need different engagement model.
-- Thresholds: High = >120% of avg revenue
--             Medium = avg to 120% of avg
--             Low = below avg
-- Concepts: Two CTEs, CASE WHEN, GROUP BY

with client_revenue as (select  client_id,
round(sum(placement_fee),0) as total_revenue,
round(avg(placement_fee),0) as avg_revenue
from placements_clean
group by client_id)

,segmented_clients as (
select client_id,
total_revenue,
avg_revenue,
case when total_revenue> (select avg(total_revenue) * 1.2 from client_revenue ) then 'High'
 when total_revenue > (select avg(total_revenue) from client_revenue) then 'Medium'
 else 'Low'
 end as value_tier
 from client_revenue
 )
 
 select value_tier,count(client_id) as client_count,round(sum(total_revenue),0) as total_revenue,
 round(avg(total_revenue),0) as avg_revenue_per_client
 from segmented_clients
 group by  value_tier
 order by value_tier

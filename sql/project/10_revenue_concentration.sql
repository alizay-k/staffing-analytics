-- Query 10: Revenue Concentration Risk
-- Business question: What percentage of total revenue
--                    comes from top 5 clients?
-- Why it matters: Over-reliance on a few clients is
--                 a business risk. If top 5 clients
--                 represent >40% of revenue, losing
--                 one client is a major financial hit.
--                 Shows business thinking beyond
--                 just technical SQL skills.
-- Concepts: Three CTEs, percentage calculation,
--           nested subqueries

with revenue_5_clients as (
select client_id,
sum(placement_fee)as total_revenue
from placements_clean group by client_id order by total_revenue desc limit 5 )

,top_5_sum AS (
    SELECT SUM(total_revenue) AS top_5_revenue
    FROM revenue_5_clients
),

 overall_revenue as(
select round(sum(placement_fee),0) as total_revenue
from placements_clean)

select (select top_5_revenue from top_5_sum) as top_5_revenue,
(select total_revenue from overall_revenue) as total_revenue,
ROUND(100.0 * (SELECT top_5_revenue FROM top_5_sum) / (SELECT total_revenue FROM overall_revenue), 1)
AS percentage_of_total;





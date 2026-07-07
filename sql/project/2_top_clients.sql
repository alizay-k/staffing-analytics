-- Query 2: Top Clients By Revenue
-- Business question: Which clients generate the most
--                    revenue and what industries are they in?
-- Why it matters: Top clients deserve priority service.
--                 Helps agency allocate senior recruiter
--                 time to highest-value relationships.
-- Concepts: JOIN, GROUP BY, SUM, AVG, COUNT, ORDER BY

select p.client_id,
c.industry,
round(sum(p.placement_fee),0) as total_revenue,
count(*) as no_of_placements,
round(avg(p.placement_fee),2) as avg_fee
from placements_clean p join clients_clean c on p.client_id=c.client_id 
group by p.client_id,c.industry order by total_revenue desc 
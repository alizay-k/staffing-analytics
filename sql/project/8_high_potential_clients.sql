-- Query 8: High Potential Clients
-- Business question: Which clients spend above average
--                    but place below average volume?
--                    These are expansion opportunities.
-- Why it matters: High-spending clients placing
--                 infrequently = untapped potential.
--                 Agency should reach out to understand
--                 what's preventing more placements.
-- Concepts: CTE, GROUP BY, HAVING with two subqueries

with client_sats as (select client_id,round(sum(placement_fee),0) as total_fee,
round(avg(placement_fee),0) as avg_fee,
count(*) as no_of_placements from placements_clean group by client_id)

select client_id,total_fee,avg_fee,no_of_placements from client_sats
where total_fee >(select avg(total_fee) from client_sats) 
and no_of_placements<(select avg(no_of_placements) from client_sats)
order by total_fee desc

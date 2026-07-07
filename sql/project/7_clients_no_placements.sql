-- Query 7: Clients With Zero Placements
-- Business question: Which clients have a contract
--                    but have never made a placement?
-- Why it matters: At-risk clients — paying a retainer
--                 but not using the service. These
--                 need a relationship check before
--                 they churn. Direct revenue risk.
-- Concepts: LEFT JOIN, IS NULL

select c.client_id,c.client_country from clients_clean c
left join placements_clean p  on p.client_id=c.client_id
where placement_id is null
-- SECTION 6: JOIN Practice Queries
-- Completed: July 2, 2026
-- Platform: CSV Fiddle
-- Dataset: placements_clean, clients_clean, 
--          recruiters_clean

--Q1: Join placements with clients
select placement_id,placement_fee,c.client_country 
from placements_clean p join clients_clean c on p.client_id=c.client_id

-- Q2: Join placements with recruiters
select placement_id,r.recruiter_id,days_to_fill from placements_clean p 
join recruiters_clean r on p.recruiter_id=r.recruiter_id

-- Q3: Left join — all clients including zero placements
select c.client_id,count(placement_id) as placement_count from clients_clean c 
left join placements_clean p on p.client_id=c.client_id group by c.client_id

-- Q4: Three-table join
select c.client_id,r.recruiter_id,placement_fee,placement_id from placements_clean p 
join clients_clean c on p.client_id=c.client_id 
join recruiters_clean r on p.recruiter_id=r.recruiter_id

-- Q5: Revenue by client country
select c.client_country,sum(placement_fee) as total_revenue from clients_clean c 
join placements_clean p on c.client_id=p.client_id group by c.client_country

-- Q6: Average fill time by recruiter seniority
select r.seniority,avg(days_to_fill) from placements_clean p 
join recruiters_clean r on p.recruiter_id=r.recruiter_id group by r.seniority 

-- Q7: Top 10 clients by total revenue
select c.client_id,sum(placement_fee) as total_fee from placements_clean p 
join clients_clean c on p.client_id=c.client_id 
group by c.client_id order by total_fee desc limit 10

-- Q8: Clients with zero placements
select c.client_id from clients_clean c 
left join placements_clean p on c.client_id=p.client_id where p.placement_id is null

-- Q9: Revenue by recruiter base country
select r.base_country,sum(p.placement_fee) as total_revenue from placements_clean p
join clients_clean c on p.client_id=c.client_id 
join recruiters_clean r on  p.recruiter_id=r.recruiter_id group by r.base_country 

-- Q10: Average fee by recruiter seniority
select r.seniority,avg(p.placement_fee) from placements_clean p 
join recruiters_clean r on p.recruiter_id=r.recruiter_id group by r.seniority order by avg(p.placement_fee) desc
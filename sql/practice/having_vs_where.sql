
select job_title,avg(placement_fee) as avg_fee from placements_clean 
group by job_title having avg_fee> 4000

select candidate_country,sum(placement_fee)as total_fee from placements_clean 
group by candidate_country having total_fee > 1000000

select recruiter_id,count(placement_id) as total_placement from placements_clean 
group by recruiter_id having total_placement > 200

select job_title,count(placement_id) as total_placements ,avg(placement_fee) as avg_fee 
from placements_clean group by job_title having total_placements>300 and avg_fee>3500
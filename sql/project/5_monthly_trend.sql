-- Query 5: Monthly Placement Trend
-- Business question: How is placement volume and
--                    revenue trending month over month?
-- Why it matters: Shows whether business is growing,
--                 flat, or declining. Essential for
--                 forecasting and budget planning.
--                 Running total shows cumulative revenue.
-- Concepts: CTE, strftime, SUM() OVER running total

with monthly_summary as(
      select 
      strftime('%Y-%m',job_post_date) as month,
      round(sum(placement_fee),0) as total_fees,
      count(*) as no_of_placements
      from placements_clean
      group by month)
      
select month,total_fees,sum(total_fees) over (order by month) as running_total,
no_of_placements
from monthly_summary
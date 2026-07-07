-- Query 4: Country Profitability and Efficiency
-- Business question: Which countries are most efficient
--                    and which are underperforming?
-- Why it matters: This is the core of the $375k ROI
--                 finding. days_vs_avg shows Pakistan
--                 fills 9.1 days faster than average.
--                 Nigeria and Kenya show negative values
--                 — costing money per placement.
-- Concepts: CTE, GROUP BY, subquery in SELECT

with info as (
select candidate_country,
      round(sum(placement_fee),0) as total_fee,
      avg(days_to_fill) as avg_days,
      count(*) as no_of_placements
      from placements_clean
      group by candidate_country)
       
select i.candidate_country,
      i.total_fee,
      i.avg_days - (select avg(days_to_fill) from placements_clean) as days_vs_avg,
      i.no_of_placements
      from info i 
      order by days_vs_avg desc

with placements as (
    select
          placement_id,
          candidate_country,
          days_to_fill,
          placement_fee_imputed
    from {{ ref('int_fees_imputed') }}
),

-- Calculate overall averages across all placements
overall as (
    select 
          avg(placement_fee_imputed) as overall_avg_fee,
          avg(days_to_fill) as overall_avg_days
    from placements
),

-- Calculate per-country metrics
country_metrics as (
    select 
         candidate_country, 
         count(placement_id) as total_placement,
         avg(days_to_fill) as country_avg_days
    from placements
    group by candidate_country
)

select 
      cm.candidate_country,
      cm.total_placement,
      round(cm.country_avg_days, 1) as avg_days,  
      
      -- Days saved vs overall average
      -- Positive = faster than average = good ROI
      round(o.overall_avg_days - cm.country_avg_days, 1) as days_saved,
      
      round(o.overall_avg_fee / o.overall_avg_days, 2) as cost_per_day,  
      
      -- Shift volume: 8% of placements NOT in this country
      cast(
          (select count(*) 
           from placements 
           where candidate_country != cm.candidate_country) * 0.08 
          as int64
      ) as shift_volume_8pct,

      round(
          (o.overall_avg_days - cm.country_avg_days) *
          (o.overall_avg_fee / o.overall_avg_days) * 
          cast(
              (select count(*) 
               from placements 
               where candidate_country != cm.candidate_country) * 0.08 
              as int64
          ),
          0
      ) as annual_roi_8pct

from country_metrics cm
cross join overall o
order by annual_roi_8pct desc
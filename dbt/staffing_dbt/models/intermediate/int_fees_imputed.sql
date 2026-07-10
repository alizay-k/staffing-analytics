with base as (
    select * from {{ref('int_placements_joined')}}
),

median as (
    select distinct 
          job_title,
          percentile_cont(placement_fee,0.5) over (partition by job_title ) as median_fees
    from base
    where placement_fee is not null
),

imputed as (
    select 
    b.*,
    coalesce(placement_fee,m.median_fees) as placement_fee_imputed

    from base b left join median m on b.job_title=m.job_title
)

select * from imputed

with source as (
    select * from {{source('staffing','recruiters_raw')}}
),

cleaned as (
    select 
          recruiter_id,
          trim(recruiter_name) as recruiter_name,
          trim(seniority) as seniority,
          trim(base_country) as base_country,
          date(hire_date) as hire_date,
          target_placements_monthly
    from source
         where recruiter_id is not null 
)

select * from cleaned
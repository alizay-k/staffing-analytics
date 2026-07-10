with placements as (
    select * from {{ref('stg_placements')}}
),

clients as (
    select * from {{ref('stg_clients')}}
),

recruiters as (
    select * from {{ref('stg_recruiters')}}
),

joined as (
    select 
    p.*,
    c.client_name,
    c.industry,
    r.recruiter_name,
    r.seniority,
    r.base_country as recruiter_country
    from placements p 
    left join clients c on p.client_id=c.client_id
    left join recruiters r on p.recruiter_id=r.recruiter_id
)

select * from joined

with source as (
    select  Distinct * from {{ source('staffing', 'placements_raw') }}
),
cleaned as (
    select 
        placement_id,
        case
            when lower(trim(job_title)) in 
                ('Senior IT Support', 'Sr. IT Support','Senior IT','Sr IT Support') then 'Senior IT Support'
            when lower(trim(job_title)) in 
                ('HR Manager','H.R. Manager','Human Resources Manager','HR Mgr') then 'HR Manager'
            when lower(trim(job_title)) in
                ('Data Analyst','Data Anlyst','Data Analysis','DataAnalyst') then 'Data Analyst'
            when lower(trim(job_title)) in 
                ('Junior Developer', 'Jr Developer','Junior Dev','Jr. Developer') then 'Junior Developer'
            else job_title
        end as job_title,
        placement_fee,
        days_to_fill,
        case 
            when lower(trim(candidate_country)) in ('pakistan', 'pak', 'pk') then 'Pakistan'
            when lower(trim(candidate_country)) in ('india', 'ind') then 'India'
            when lower(trim(candidate_country)) in ('philippines', 'ph') then 'Philippines'
            when lower(trim(candidate_country)) in ('kenya', 'ken') then 'Kenya'
            when lower(trim(candidate_country)) in ('nigeria', 'ng') then 'Nigeria'
            else candidate_country
        end as candidate_country,
        trim(client_country) as client_country,
        client_id,
        recruiter_id,
        date(job_post_date) as job_post_date,
        date(fill_date) as fill_date
    from source
    where placement_id is not null
)

select * from cleaned  
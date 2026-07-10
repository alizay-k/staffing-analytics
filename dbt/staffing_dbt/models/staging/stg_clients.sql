with source as (
    select  * from {{source('staffing','clients_raw')}}

),

cleaned as (
    select 
          client_id,
          trim(client_name) as client_name,
          trim(industry) as industry,
          trim(client_country) as client_country,
          date(contract_start) as contract_start,
          monthly_retainer

    from source
        where client_id is not null

)

select * from cleaned
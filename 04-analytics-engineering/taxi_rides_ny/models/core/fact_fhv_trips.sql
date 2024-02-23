{{
    config(
        materialized='table'
    )
}}

with fhv as (
    select *, 
    from {{ ref('stg_fhv') }}
), 
dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)
select 
fhv.tripid,
fhv.pickup_locationid,
fhv.dropoff_locationid,
fhv.pickup_datetime,
fhv.dropoff_datetime,
fhv.dispatching_base_num,
fhv.sr_flag,
fhv.affiliated_base_number,
pickup_zone.borough as pickup_borough, 
pickup_zone.zone as pickup_zone, 
dropoff_zone.borough as dropoff_borough, 
dropoff_zone.zone as dropoff_zone
from fhv
inner join dim_zones as pickup_zone
on fhv.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv.dropoff_locationid = dropoff_zone.locationid
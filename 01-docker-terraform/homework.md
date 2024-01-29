## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`

### ✔ Answer:
```      --rm                             Automatically remove the container when it exits```

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?



#### option 1 
``` docker run -it --rm --entrypoint bash python:3.9 list``` and then ```pip list```

 #### option 2 
 ``` docker run -it --rm --entrypoint pip python:3.9 list```

 #### (explanation)
 
- docker run: Initiates a Docker container.
- -it: Allocates a pseudo-TTY for interactive mode.
- --rm: Removes the container automatically upon completion.
- --entrypoint pip: Overrides the default entrypoint and sets it to pip.
- python:3.9: Specifies the base Docker image as Python 3.9.
- list: Executes the pip list command inside the container.


### ✔ Answer
- 0.42.0

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

### ✔ How to do:
Because  i've followed the videos the best option for me is: 
```bash 
docker-compose up
```
it will run container for pgdatabase and pgadmin

save somewhere host name from docker-compose log to use it in ingestion command.
host is the name of the database container
```bash
[+] Building 0.0s (0/0)                                                                                                                                                                                                          docker:default
[+] Running 2/0
 ✔ Container 2_docker_sql-pgdatabase-1  Created                                                                                                                                                                                            0.0s 
 ✔ Container 2_docker_sql-pgadmin-1     Created                                                                                                                                                                                            0.0s 
Attaching to 2_docker_sql-pgadmin-1, 2_docker_sql-pgdatabase-1
```

then for ingesting data we need network 

```bash
docker network ls
```

```
NETWORK ID     NAME                   DRIVER    SCOPE
d757a7b743d4   2_docker_sql_default   bridge    local
```

I use this [dataloader.py](https://github.com/thebadcoder96/DataEngineering/blob/436576dee50f9b497b1546e3ac64976af46eb7ca/1_week/1_Docker_SQL/data-loading.py) to ingest new data using [dockerfile](https://github.com/thebadcoder96/DataEngineering/blob/436576dee50f9b497b1546e3ac64976af46eb7ca/1_week/1_Docker_SQL/Dockerfile). Thank you @thebadcoder96!  
 
```bash
docker build -t dataload:0.1 .
```

then update [this](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/2_docker_sql/README.md#data-ingestion) original command for our url, network, host

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

docker run -it \
  --network=2_docker_sql_default \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_2019_09_taxi_trips \
    --url=${URL}
```
 output
 ```bash
Downloading green_tripdata_2019-09.csv.gz ...
--2024-01-29 00:04:56--  https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz
Resolving github.com (github.com)... 140.82.121.4
Connecting to github.com (github.com)|140.82.121.4|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://objects.githubusercontent.com/github-production-release-asset-2e65be/513814948/b5af7693-2f26-4bd5-8854-75edeb650bae?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20240129%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240129T000456Z&X-Amz-Expires=300&X-Amz-Signature=d638a33aa67276370a44b3477888961472f3d9bacd60f8311c51f3e370185e9a&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=513814948&response-content-disposition=attachment%3B%20filename%3Dgreen_tripdata_2019-09.csv.gz&response-content-type=application%2Foctet-stream [following]
--2024-01-29 00:04:56--  https://objects.githubusercontent.com/github-production-release-asset-2e65be/513814948/b5af7693-2f26-4bd5-8854-75edeb650bae?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20240129%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240129T000456Z&X-Amz-Expires=300&X-Amz-Signature=d638a33aa67276370a44b3477888961472f3d9bacd60f8311c51f3e370185e9a&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=513814948&response-content-disposition=attachment%3B%20filename%3Dgreen_tripdata_2019-09.csv.gz&response-content-type=application%2Foctet-stream
Resolving objects.githubusercontent.com (objects.githubusercontent.com)... 185.199.111.133, 185.199.109.133, 185.199.110.133, ...
Connecting to objects.githubusercontent.com (objects.githubusercontent.com)|185.199.111.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 7854533 (7.5M) [application/octet-stream]
Saving to: ‘green_tripdata_2019-09.csv.gz’

green_tripdata_2019-09.csv.gz                               100%[===========================================================================================================================================>]   7.49M  9.85MB/s    in 0.8s    

2024-01-29 00:04:58 (9.85 MB/s) - ‘green_tripdata_2019-09.csv.gz’ saved [7854533/7854533]



inserting batch 1...
inserted! time taken     31.578 seconds.

inserting batch 2...
inserted! time taken     28.379 seconds.

inserting batch 3...
inserted! time taken     14.731 seconds.

/app/data-loading.py:48: DtypeWarning: Columns (3) have mixed types. Specify dtype option on import or set low_memory=False.
  for batch in df_iter:
inserting batch 4...
inserted! time taken     12.060 seconds.

inserting batch 5...
inserted! time taken      5.375 seconds.

Completed! Total time taken was     95.919 seconds for 5 batches.
```





## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- 15612
- 15859
- 89009

### ✔ Answer
15612

```sql
SELECT count(*)
FROM 
green_2019_09_taxi_trips g
where cast(g.lpep_pickup_datetime as DATE)= '2019-09-18' and
cast(g.lpep_dropoff_datetime as DATE)= '2019-09-18'

LIMIT 100
```

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21

### ✔ Answer
2019-09-26

```sql
SELECT 
max(g.trip_distance) as max_dist,
cast(g.lpep_pickup_datetime as DATE) as pickup_time
FROM green_2019_09_taxi_trips g
group by pickup_time
order by max_dist DESC
limit 1
```

## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

### ✔ Answer

"Brooklyn" "Manhattan" "Queens"


```sql
SELECT 
"Borough",
sum(green.total_amount) as sum_total
FROM zones z
inner join public.green_2019_09_taxi_trips green on
    green."PULocationID"=z."LocationID"
    where CAST(green.lpep_pickup_datetime as DATE) ='2019-09-18'
group by "Borough"
having sum(green.total_amount)>50000;
```


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza

### ✔ Answer

"JFK Airport"

```sql
SELECT 
"tip_amount",
green."PULocationID" as pickup_location,
pu_z."Zone",
green."DOLocationID" as dropoff_location,
do_z."Zone"
FROM public.green_2019_09_taxi_trips green
inner join zones pu_z
on green."PULocationID"=pu_z."LocationID"
inner join zones do_z on
 green."DOLocationID"=do_z."LocationID"
 
where pu_z."Zone" ='Astoria' 
order by green.tip_amount DESC
limit 1;

```



## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

### ✔ Answer
```bash

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "de-zoomcamp-412419"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "de-zoomcamp-terraform-demo-terra-bucket-a1"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

```
Paste the output of this command into the homework submission form.


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET

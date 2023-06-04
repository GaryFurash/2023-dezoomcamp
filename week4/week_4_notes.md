# Week 4 Notes - Analytic Engineering

[Power Point](./materials/week_4_analytics%20engineering.pptx)
[Week Summary](./materials/README.md)

## 4.1.1 Introduction to analytics engineering

 * What is analytics engineering?
 * ETL vs ELT
 * Data modeling concepts (fact and dim tables)

[4.1.1 Video](https://www.youtube.com/watch?v=uF76d5EmdtU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=33)

### Stages

* Loading (Fivetran, Stitch)
* Storage (Snowflake, BigQuery, RedShift)
* Modeling (Dataform, DBT)
* Presentation (Power BI, Tableau)

### ELT vs ELT

[ELT vs ETL](../images/w4s01.png)

### Dimensional Modeling

Dimensional Modeling prioritizes understandability and usability over normalization (minimizing redundancy)

Star Schema / Fact and Dimensional

**Fact Tables**
* Measurements, metrics, or facts (numeric)
* Describes the outcome or state of a *business process*
* Verbs ("Sales")
* Point in time

**Dimension Tables**
* Business *entities*
* Nouns
* Describe the context of the measurement described in a fact
* Persistent

Kimball distinguishes between areas:
Staging Area (raw data) -> Processing Area (interim activities) -> Presentation (exposed to stakeholder)

## 4.1.2 What is DBT

[4.1.2 What is dbt](https://www.youtube.com/watch?v=4eCouvVOJUw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=32)

DBT (Data Built Tool) is used for Transformation, moving from the raw data (lake) to the transformed data consumed by BI tools and the like. It supports good software practices like CI/CD Deployment / Versioning, Testing, and Documentation

[dbt](./images/w4s02.png)

Your *model* QUERY transformed by dbt into DML

*Macros*: functions

## 4.2.1 Starting a dbt Product

[4.2.1 Starting a dbt Product](https://www.youtube.com/watch?v=iMxh6s_wL4Q&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=33)

### Setting up the Lake Data

> My taxi data was loaded into gcs with etl_web_to_gcs.py script that converts csv data into parquet. Then I placed raw data trips into external tables and when I executed dbt run I got an error message: Parquet column 'passenger_count' has type INT64 which does not match the target cpp_type DOUBLE. It is because several columns in files have different formats of data. When I added df[col] = df[col].astype('Int64') transformation to the columns: passenger_count, payment_type, RatecodeID, VendorID, trip_type it went ok.

I implemeted this by putting logic between the read of the downloaded CSV and the write to a parquet file.

```python
# read the CSV file and correct type inferences
df = pd.read_csv(file_name, compression='gzip')
# for col_name in df.columns:
#    print(col_name)
# quit()
df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
df['passenger_count'] = df['passenger_count'].astype('Int64')
df['payment_type'] = df['payment_type'].astype('Int64')
df['RatecodeID'] = df['RatecodeID'].astype('Int64')
df['VendorID'] = df['VendorID'].astype('Int64')
df['trip_type'] = df['trip_type'].astype('Int64')

# write it to a parquet file
file_name = file_name.replace('.csv.gz', '.parquet')
df.to_parquet(file_name, engine='pyarrow')
```

The *low_memory* warning during pandas load is because guessing dtypes for each column is very memory demanding. Pandas tries to determine what dtype to set by analyzing the data in each column. Ideally would would specify up front what the values are as ```pd.read_csv(sio, dtype={"user_id": int, "username": "string"})```

I then created 2 datasets in BigQuery, ```dbt_models`` (staging) and ``trips_data_all``. I then created exernal tables referencing the parquet data.

```sql
CREATE OR REPLACE EXTERNAL TABLE `trips_data_all.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://gffurash-prefect-de-zoomcamp/green/green_tripdata_*.parquet']
);
```

### Using dbt

Using a dbt docker image, you can create a project specifying the working directory (which will contain a hierarchy of folders), the name of the project, and `init` (or otherwise cd into the 'project directory' ```dbt init```)

```bash
docker compose run --workdir="//usr/app/dbt/taxi_rides_ny" dbt-bq-dtc init
```

This will also create your `dbt_project.yml` file, which manages the global settings (e.g., database), variables, and settings.

```~\.dbt\profiles.yml``` (which is mapped in my ```docker-compose.yaml``` as ```- ~/.dbt/:/root/.dbt/```) contains database connections to connect to a data warehouse and one or more targets in the database (includes credentials setup).

```bash
bq-dbt-workshop:
  outputs:
    dev:
      dataset: polar-column-380322.dezoomcamp
      fixed_retries: 1
      keyfile: /.google/credentials/google_credentials.json
      location: US
      method: service-account
      priority: interactive
      project: polar-column-380322
      threads: 4
      timeout_seconds: 300
      type: bigquery
      dataset: dbt_models
  target: dev
```

You then link your ```dbt_project.yml``` to a profile by adding a reference to a top-level entry like ```profile: 'bq-dbt-workshop'```

**profile**: defines which database is being used in this project. dbt understands how to build SQL and DML for different databases.

**vars**: global variables

## 4.2.2 Starting local dbt project

[4.2.2 Starting local dbt project](https://www.youtube.com/watch?v=1HmL63e-vRs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=34)

```dbt init``` creates a project interactively with all of the necesary subdirectories. You need to modify the

```dbt debug``` will test your configuration and connections

## 4.3.1 Build a dbt Model

[## 4.3.1 Build a dbt Model](https://www.youtube.com/watch?v=UVI30Vxzd6c&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=35)

```{{}}``` is a ?chinga? block - you can use macros here

[w4s04](../images/w4s04.png)

### Materialization Strategy

First, identify the materialization strategy (table, view, incremental, ephemeral).

| Stragegy    | Usage                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------------ |
| table       | drop and recreate the table with the name of the model in the target schema (= BigQuery dataset) |
| view        | create or alter view in target schema                                                            |
| incremental | allows you to insert the latest data (like a cte)                                                |

### From Clause

[w4s05][../images/w4s05.jpg]

```{source('schema/dataset', 'table')}``` allows you to define sources in a yaml file that allows you to configure the database (Big Query dataset) and schema along with the sources

dbt to BigQuery terminology
| dbt      | BigQuery   |
| -------- | ---------- |
| database | project id |
| schema   | dataset    |
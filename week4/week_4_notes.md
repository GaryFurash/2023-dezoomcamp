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

```{{[macro]}}``` is a [Jinja](https://realpython.com/primer-on-jinja-templating/) block - you can use macros (functions) here.

[w4s04](../images/w4s04.png)

dbt to BigQuery terminology
| dbt      | BigQuery   |
| -------- | ---------- |
| database | project id |
| schema   | dataset    |

### Materialization Strategy

First, identify the materialization strategy (table, view, incremental, ephemeral).

| Stragegy    | Usage                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------------ |
| table       | drop and recreate the table with the name of the model in the target schema (= BigQuery dataset) |
| view        | create or alter view in target schema                                                            |
| incremental | allows you to insert the latest data (like a cte)                                                |
| ephemeral   |                                                                                                  |

### From Clause

[w4s05][../images/w4s05.png]

```{source('dataset', 'table')}``` allows you to define sources in a yaml file that allows you to configure the database (Big Query dataset) and schema along with the sources. This macro refers to entries in the `sources:` section of the YAML.

`freshness:` block define`s the acceptable amount of time between the most recent record, and now, for a table to be considered "fresh". In the freshness block, one or both of warn_after and error_after can be provided.

*seeds*. CSV files stored under ```seeds``` folder. Stored in repository (and versioned), for relatively static data. Use ```dbt seed {-s file_name}```. Call via ```from {{ ref('filename.csv') }}```

*ref*: macro that references undelying table and views. It references the yml file to resolve the actual project.dataset.table path based on current enviornment.

[staging](../week4/materials/taxi_rides_ny/models/staging/) contains the raw models. Built as views so they don't need to be refreshed.

```SQL
SELECT * FROM `polar-column-380322.trips_data_all.external_yellow_tripdata` LIMIT 1
SELECT * FROM `[dataset].[schema].[table]` LIMIT 1
```

```yaml
# if record_loaded_at field is more than 6 hours in the source then refresh.
# No data will be older than 6 hours.
loaded_at_field: record_loaded_at
    tables:
      - name: external_green_tripdata
      - name: external_yellow_tripdata
        freshness:
          error_after: {count: 6, period: hour}
```

```yaml
sources:
    - name: staging
      database: polar-column-380322
      schema: trips_data_all
```

In ```schema.yml``` will Clause

``` from {{ source('staging','external_green_tripdata') }} ```

to resolve to

``` from `polar-column-380322.trips_data_all.external_green_tripdata` ```

[core](../week4/materials/taxi_rides_ny/models/core/) contains the models that will be exposed to the BI tool

Execute via ```dbt run -m stg_green_tripdata``` (model.sql) or ```dbt run``` to run all models.

sql files under {project}\models\{zone} define the tables being created, returning SELECT results. Run a specific select via ```dbt run --select {sql file name}```

### Macros

[w4s06](..\images\w4s06.png)

Written in **jinja**. dbt includes many macros. placed under {project}\macros w/ ```.sql``` extension.

```
{# returns the description of the payment_type #}

{% macro get_payment_type_description(payment_type) -%}

    case {{ payment_type }}
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
    end

{%- endmacro %}
```

The above passes in a payment type, then resolves to a block of SQL code Wwhen called as

```select {{ get_payment_type_description('payment_type') }} as payment_type_description```

```run``` causes the compiled output to be placed in a ```Target``` subdirectory for review.

### Packages

Share macros between projects

[w4s07](..\images\w4s07.png)

```{project}\packages.yaml``` lists the packages to include. Prefixed macros using with the lowest level package name. Run ```dbt depts``` to download packages (not done automatically on first run).

```{dbt_utils.surrogate_key}(<columns>)``` is used to create a unique key for the model (table) using a hash on the concatenated value.

### Variables

[w4s08](..\images\w4s08.png)

Substituted at compleation time.

1. Define in Project (global) level in dbt_project.yml
2. Reference using ```var``` macro, and then pass in dbt command line via ```--var '{name}: value'```


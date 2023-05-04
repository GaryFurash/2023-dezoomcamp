# Week 3 - Data Warehouse

* Data Warehouse
* BigQuery
* Partitioning and clustering
* BigQuery best practices
* Internals of BigQuery
* Integrating BigQuery with Airflow
* BigQuery Machine Learning

## Reference & Links

[Week 3 ReadMe](./materials/ReadMe.md)
[Video 3.1.1](https://www.youtube.com/watch?v=jrHljAoD6nM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=25)
[Big Query SQL](./materials/big_query.sql)
[Video 3.1.1](https://www.youtube.com/watch?v=-CqXf7vhhDs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=26)

## 3.1.1 Data Warehouse and BigQuery

BigQuery is our example Data Warehouse.

### Overview

*OLAP VS OLTP:*

![OLAP vs OLTP](../images/w3s01.png)
![OLAP vs OLTP](../images/w3s02.png)

Data Warehouse Structure:

* [1:M] Data Sources
  * -> Staging Area
    * -> Warehouse Structures
      * -> Data Marts
      * -> End Users
      * -> Machine Learning

BigQuery advantages are:
  * serverless + embedded infrastructre (scalable)
  * built in machine learning, geospatial analysis

By default CACHES queries

Creating external table *referring* to a Google Cloud Storage bucket. Schema is defined on write.

```sql
CREATE OR REPLACE EXTERNAL TABLE `taxi-rides-ny.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://nyc-tl-data/trip data/yellow_tripdata_2019-*.csv', 'gs://nyc-tl-data/trip data/yellow_tripdata_2020-*.csv']
);
```

### Partitioning & CLustering

Select *partition* rule based on most common *filter* columns -> improves performance and scalablility by reading less data. Patitioning "under the covers" creates multiple storage locations based on the rule (where all data matching the rule resides).

```sql
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_non_partitoned AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitoned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```

*Clustering* groups data by columns within a partition.

```sql
-- Creating a partition and cluster table. In this example we usually use
-- VendorID as a 2nd filter
CREATE OR REPLACE TABLE taxi-rides-ny.nytaxi.yellow_tripdata_partitoned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM taxi-rides-ny.nytaxi.external_yellow_tripdata;
```

## 3.1.2 Partitioning and Clustering

< 1 GB Partitioning and Clustering don't help

Partitioning

* Time Unit Columns
* Ingestion Time (_PARTITIONTIME)
  * Daily/hourly/monthly/yearly - choose course grain first
  * Max number of Partitioning 4000 / table - use *expire*
* Integer Range Partitioning
* Allows management (e.g., dropping)

Clustering

* Columns co-locate location
* Determines sort order in column sequence
* Max 4 columns - top-level, not-repeated

When to Cluster vs Partition

* Choose when more filters and granularity needed
* Partitioning would provide too small sections (1 GB)
* Partitioning would create too many partitions
* Updates frequently modify MANY partition

Auto Re-Clustering
* Writes are often to blocks with key ranges not in existing blocks
* BigQuery automatically re-clusters int he background
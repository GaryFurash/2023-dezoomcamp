# Week 3 Homework Notes

[Homework Instructions](../materials/homework.md)
[Homework Solution](https://www.youtube.com/watch?v=j8r2OigKBWE)

## Load the Data into GCS Cloud Storage and Create Structures

Manually loaded into
dtc_dezoomcamp (project)
gffurash-prefect-de-zoomcamp > data > fhv

Navigate to GCS Storage > Buckets > Configuration and fetch the URI

```
gs://gffurash-prefect-de-zoomcamp/data/flv/flv_tripdata_2019-01.csv.gz
```

Navigate to GCS > Big Query and at the root of your project create a dataset (```hw```)

![w3s06.png](../../images/w3s06.png)

Create the external table referencing ```[your project].[dataset].[table name]```. You can get the URI by right clicking on a object (gzip file) in Buckets and get its Configuration.

```SQL
CREATE OR REPLACE EXTERNAL TABLE polar-column-380322.hw.fhv_external_table
OPTIONS (
  format = 'CSV',
  uris = ['gs://gffurash-prefect-de-zoomcamp/data/fhv/*.csv.gz']
);
```

It should return ```This statement created a new table named fhv_external_table.```

Then create the materialized table based on that external table

```SQL
CREATE OR REPLACE TABLE polar-column-380322.hw.fhv_materialized_table
AS
(
    SELECT * FROM polar-column-380322.hw.fhv_external_table
)
```

This will take a while as it proceses the files. When complete it should return ```This statement created a new table named fhv_materialized_table.```

## Question 1 What is the count for fhv vehicle records for year 2019?

- 43,244,696

## Question 2 Write a query to count the distinct number of affiliated_base_number for the entire dataset on both the tables.

```SQL
SELECT COUNT(DISTINCT(Affiliated_base_number))
FROM polar-column-380322.hw.fhv_external_table;
```

Result: 0 bytes, can't estimate

```SQL
SELECT COUNT(DISTINCT(Affiliated_base_number))
FROM polar-column-380322.hw.fhv_materialized_table;
*/
```

Result: 317.94 MB estimate

## Question 3 How many records have both a blank (null) PUlocationID and DOlocationID in the entire dataset?

717,748

## Question 5 What is the best strategy to optimize the table if query always filter by pickup_datetime and order by affiliated_base_number?

If you are going to filter on an integer or date-like value, then *Partitioning* is probably the correct choice. *Ordering* will be better setup for clustering (which couldn't be used anyway so can't be partitioned)

Partition by pickup_datetime, cluster by affiliated_base_number.

## Question 5: Implement the optimized solution you chose for question 4. Write a query to retrieve the distinct affiliated_base_number between pickup_datetime 2019/03/01 and 2019/03/31 (inclusive).

```SQL
CREATE OR REPLACE TABLE polar-column-380322.hw.fhv_materialized_table_reorganized
PARTITION BY DATE(pickup_datetime)
CLUSTER BY affiliated_base_number AS
SELECT * FROM polar-column-380322.hw.fhv_materialized_table;
```

Given the query

```SQL
SELECT COUNT( DISTINCT (affiliated_base_number ) )
FROM polar-column-380322.hw.fhv_materialized_table_reorganized
WHERE pickup_datetime between '2019-03-01' and '2019-03-31';

SELECT COUNT( DISTINCT (affiliated_base_number ) )
FROM polar-column-380322.hw.fhv_materialized_table
WHERE pickup_datetime between '2019-03-01' and '2019-03-31';
```

The reorganized table will process 23.05 MB, and the original table will 647.87 MB.

## Question 6: Where is the data stored in the External Table you created?

The external table remains in GCP bucket

## Question 7: Is it best practice to always cluster your data?

No. Particularly with small sets of data GCP.

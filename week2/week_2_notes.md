# Week 2 Notes

* Data Lake
* Workflow orchestration
* Introduction to Prefect
* ETL with GCP & Prefect
* Parametrizing workflows
* Prefect Cloud and additional resources
* Homework

**Links**

* [Week 2 Prefect](https://github.com/discdiver/prefect-zoomcamp)
* [transcript with code for the second Prefect video](https://github.com/discdiver/prefect-zoomcamp/tree/main/flows/01_start)
* [fifth Prefect video](https://github.com/discdiver/prefect-zoomcamp/tree/main/flows/01_start)
* [padilha notes](https://github.com/padilha/de-zoomcamp/tree/master/week2)

## Data Lake

[DE Zoomcamp 2.1.1 - Data Lake](https://www.youtube.com/watch?v=W3Zm6rjOq70&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

### What is a Data Lake

Goal: make data as accessible as possible as quickly as possible, particularly non-standard data sources

* Contains data from multiple sources
* Contains data of multiple types (structured, unstructured, semi-structured)
* Includes metadata as data is added (Index and Catalog)
* Highly scalable, Inexpensive hardware

![Data Lake Features](../images/w2s01.png)

![Comparison](../images/w2s02.png)


| Area          | Data Lake                             | Data Warehouse                 |
| ------------- | ------------------------------------- | ------------------------------ |
| *Data Format* | Raw data in multiple formats          | Highly structured cleaned data |
| *Users*       | Data Scientists, Machine Learning     | Business, Analysts             |
| *Volume*      | Massive volumes                       | Curated volumes                |
| *Speed*       | Very fast (no design time, streaming) | Normal business cycle          |

### ETL vs ELT

| ELT                        | ETL                       |
| -------------------------- | ------------------------- |
| Extract Load and Transform | Export Transform and Load |
| Massive volumes            | Smaller volumes           |
| *Schema on Read* (source)  | Pre-defined target schema |
| Lake                       | Warehouse                 |

### Risks

* Data swamp (no versioning, inconsistent schemas)
* Joins are difficult (quality, structure)

### Providers

| Provider | Product       |
| -------- | ------------- |
| GCP      | Cloud Storage |
| AWS      | S3            |
| Azure    | Azure Blob    |

## State of Data Engineering

![](../images/w2s03.jpg)

## 2.2.1 Introduction to Workflow Orchestration

[Introduction to Workflow Orchestration](https://www.youtube.com/watch?v=8oLs6pzHp68&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=18)

* Governing your data flow in a way that respects coordination rules
* Orchestration tools let you turn code into a workflow that can be scheduled and observed
* Delivery System Analogy
  * Products in Boxes = Tasks in Workflow
  * Order in Cart = Workflow. Do they get delivered all at once, sequentially, independently, parallelization, concurrency and asynch
  * Delivery = Workflow Orchestration. Schedule, scaleable, guaranteed despite issues, observable, secured

## 2.2.2 Introduction to Prefect Concepts

[Introduction to Prefect Concepts](https://www.youtube.com/watch?v=cdtN6dhp708&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&ironments
[Code Examples](https://github.com/discdiver/prefect-zronments

Prefect is a Python based Orchestration application

Install python packages from file in *[package]=[version]. Using a virtual environment isolates the configuration and packages needed for your python project rather than installing them into your system.

```bash
# install delivered utility for virutal environments
sudo apt-install python3.10-venv
# in directory from which you want setup the virtual environment
python -m venv zoomcamp
#  within the directory that you just issued that command, activate it
source ./zoomcamp/bin/activate
# install pip packages from a file (version specified)
pip install -r requirements.txt
# deactivate
deactivate
```

### Example Ingestion Script

[Simple Ingestion Script](./materials/ingest_data_flow_1.py)

* FLOW is a function-like container of workflow logic
* FLOWS contain TASKs
* TASKs can receive information about upstream dependencies and the state of the dependency
* before runs. This allows tasks to wait on the completion of other tasks
  * Additional Elements: print log, set retries

**Step 1**: Transform ingest_data.py into a Prefect flow. For such, we move all code under if __name__ == '__main__ to a function main_flow(). Then, we use the flow decorator to indicate that main_flow() is a Prefect flow. According to the instructor, a flow consists of a container for workflow logic that we can use to interact and understand the state of the workflow. They receive inputs, perform a set of tasks and returns outputs. In addition, we use the @task decorator to indicate that ingest() is a task from our flow. See [ingest_data_flow_1.py](./work/ingest_data_flow_1.py). Then, we run this new code:

```bash
python ingest_data_flow_1.py
```

Which generates

```bash
17:51:40.362 | INFO    | prefect.engine - Created flow run 'platinum-gopher' for flow 'Ingest Data'
17:51:40.507 | INFO    | Flow run 'platinum-gopher' - Created task run 'extract-bb1266fe-0' for task 'extract'
17:51:40.508 | INFO    | Flow run 'platinum-gopher' - Executing 'extract-bb1266fe-0' immediately...
17:51:41.468 | INFO    | Task run 'extract-bb1266fe-0' - Finished in state Completed()
17:51:41.493 | INFO    | Flow run 'platinum-gopher' - Created task run 'transform-a7d916b4-0' for task 'transform'
17:51:41.493 | INFO    | Flow run 'platinum-gopher' - Executing 'transform-a7d916b4-0' immediately...
17:51:41.531 | INFO    | Task run 'transform-a7d916b4-0' - pre: missing passenger count: 26726
17:51:41.611 | INFO    | Task run 'transform-a7d916b4-0' - post: missing passenger count: 0
17:51:41.635 | INFO    | Task run 'transform-a7d916b4-0' - Finished in state Completed()
17:51:41.659 | INFO    | Flow run 'platinum-gopher' - Created task run 'load-60b30268-0' for task 'load'
17:51:41.659 | INFO    | Flow run 'platinum-gopher' - Executing 'load-60b30268-0' immediately...
17:52:58.989 | INFO    | Task run 'load-60b30268-0' - Finished in state Completed()
17:52:59.015 | INFO    | Flow run 'platinum-gopher' - Finished in state Completed('All states completed.')
```

**Step 2**: transform the script into ETL. Currently, the code performs everything all at once. We can break ingest() into three different tasks: Extract (E), Transform (T) and Load (L). See [ingest_data_flow_etl.py](./work/ingest_data_flow_etl.py) and [ingest_data_flow.py](./materials/ingest_data_flow.py). The flow decorated method coordinates the tasks

```python
@flow(name='Ingest Data')
def main_flow(args):
    url = args.url
    raw_data = extract(url)
    data = transform(raw_data)
    load(user, password, host, port, db, table_name, data)
```

Since tasks may be run multiple times you can improve performance with *caching*

```python
  from prefect.tasks import task_input_hash
  from datetime import timedelta

  @task(log_prints=True, tags=["extract"], cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
```

Tasks are just functions and so therefore can be parameterized, for example making the table name

```python
# define a flow that takes a string parameter
@flow(name="Ingest Data")
def main_flow(table_name: str = "yellow_taxi_trips"):
    csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
    log_subflow(table_name)

if __name__ == '__main__':
    # pass the name of the table to the main_flow task
    main_flow(table_name="yellow_trips")
```

**Step 4**: we can use *prefect orion* to view our workflows and define configuration external to the script.

Prefect Orion UI allows us to see our flows in an interactive an intuitive web interface. It summarizes the state of our workflows. Besides, we also have some extra information, such as:

Task Run Concurrency, which can be configured by adding tags to tasks.

Notifications, that alerts us when something goes wrong.

Blocks, which allows us to store configurations and use them as an interface for interacting with external systems. In other words, we can securely store authentication credentials for different services, without the need to specify such credentials directly in our codes or command lines.

```bash
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect orion start
```
Create a new block for our PostgreSQL connector. In Prefect Orion UI, we first click in "Blocks" and then "Add Block +". Next, we add a SQLAlchemyConnector, and fill the corresponding form as follows and click on "Create". This one uses single thread postgres-psycopy2

![block](../images/w2s03.png)

**Step 6**: use the block in the code using this snippet (see [ingest_data_flow_etl_with_sql_block.py](./work/ingest_data_flow_etl_with_sql_block.py))

```python
from prefect_sqlalchemy import SqlAlchemyConnector

with SqlAlchemyConnector.load("postgres-connector") as database_block:
    with connection_block.get_connection(begin=False) as engine:
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')
```

[Integrations](http://docs.prefect.io/collections/catalog) are organized into collections of pre-built tasks, flows, blocks and more that are installable as PyPI packages.

## 2.2.3 ETL with GCP and Prefect
[DE Zoomcamp 2.2.3 - ETL with GCP & Prefect](https://www.youtube.com/watch?v=W-rMz_2GwqQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=20)

Start your venv that you created with the contents of requirements.txt

```bash
. ./zoomcamp/bin/activate
```

In a separate terminal window (using the same venv) start orion server (you must do this as this is is panda's run time environment)

```bash
prefect config set PREFECT_API_URL="http://127.0.0.1:4200/api"
prefect orion start
```

See [etl_web_to_gcs.py](./materials/etl_web_to_gcs.py) for code that performs the load into GCP

Set retries with steps that have connections (that might fail)

```python
@task(retries=3)
```

Given the path to the file write it to Google Cloud Storage bucket. This assumes you've [setup](week1/week1_notes2.md) a GCP account, your GCP tools, and setup local authentication.

Navigate to your GCP Project, then Google Cloud Storage > Buckets. Create a new bucket. The name has to be GLOBALLY unique (not just to your project). This can also be done from the command line. In this example I created "gffurash-prefect-de-zoomcamp"

Prefect *blocks* yet you store reusable configuration information. Where Orion is already running, add the block elements for Google cloud.

```bash
prefect block register -m prefect_gcp
```

![w2s04.png](../images/w2s04.png)

Navigate to your [Orion Server](http://http://127.0.0.1:4200/) and go to Blocks and select GCS Bucket +. When creating the bucket add credentials to access via your service account.

If you haven't created service account yet, go to Google Cloud > IAM & Admin > Service Accounts and Create Service Account. Give it roles (at minimum) BigQuery Admin and Cloud Storage > StorageAdmin. On the row click Keys and Create New Key in JSON format. This document shouldn't be stored in a public repository.

Once you've downloaded the JSON file open it up and cut and paste the contents into a new GCS Credentials block.

```python
from prefect_gcp import GcpCredentials
gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
```

![w2s05.png](../images/w2s05.png)

Create a new GCS Bucket block and reference the GCS Credentials block.

![w2s06.png](../images/w2s06.png)

```python
from prefect_gcp.cloud_storage import GcsBucket
gcp_cloud_storage_bucket_block = GcsBucket.load("zoom-gcs")
```

Reference that block in your code

```python
@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return
```

On execution you will get something like this

```bash
15:48:58.370 | INFO    | Flow run 'neon-wren' - Created task run 'write_gcs-1145c921-0' for task 'write_gcs'
15:48:58.370 | INFO    | Flow run 'neon-wren' - Executing 'write_gcs-1145c921-0' immediately...
15:48:58.469 | INFO    | Task run 'write_gcs-1145c921-0' - Getting bucket 'gffurash-prefect-de-zoomcamp'.
15:48:58.848 | INFO    | Task run 'write_gcs-1145c921-0' - Uploading from PosixPath('data/yellow/yellow_tripdata_2021-01.parquet') to the bucket 'gffurash-prefect-de-zoomcamp' path 'data/yellow/yellow_tripdata_2021-01.parquet'.
15:49:03.748 | INFO    | Task run 'write_gcs-1145c921-0' - Finished in state Completed()
15:49:03.776 | INFO    | Flow run 'neon-wren' - Finished in state Completed('All states completed.')
```
and the file is now in cloud_storage

![w2s07.png](../images/w2s07.png)

## 2.2.4 From Google Cloud Storage to Big Query

[2.2.4 From Google Cloud Storage to Big Query](https://www.youtube.com/watch?v=Cx5jt-V5sgE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=22)

Moving from Data Lake (Google Cloud Storage) to Data Warehouse (Big Query)

### Setup Google BigQuery Target Table

Create a table to load the data into in Google Big Query using an existing Parquet file.

BigQuery > + Add Storage > + Google Cloud Storage. Reference the existing GCS bucket and create a data source

![w2s08](../images/w2s08.png)

This starts a load job which will build a table based on the sample dataset loaded

![w2s09](../images/w2s09.png)

Now delete the data since it was only used to create the table (using the Query tab)

```sql
DELETE FROM `polar-column-380322.dezoomcamp.rides` WHERE true
```

### Load data into BigQuery

See [etl_gcs_to_bq.py](./materials/etl_gcs_to_bq.py)

Note all reference are based on the bucket definition in Orion - that's how the script knows information about the account and GCS location (e.g., zoom-gcs - there isn't any name "zoom-gcs" in the Google cloud account).

Retrieving from GCS - this actually downloads it to the current directory.

```python
@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download object from GCS storage and return path to it"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")
```

Convert parquet file to DataFrame and cleanup null values

```python
@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    df["passenger_count"].fillna(0, inplace=True)
    print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df
```

```python
@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")
    # to_gbq is a Pandas method
    df.to_gbq(
        destination_table="dezoomcamp.rides",
        # set the project ID and table to match your Google setup
        project_id="polar-column-380322",
        # retreive the service account credentials sotored in the Prefect block
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )
```

To run (1) activate the venv built with [reqirements.txt](../materials/requirements.txt), (2) start the Orion server, (3) then in a separate terminal (with environment activated) run python ./../[file.py]

## 2.2.5 Parametrizing Flow & Deployments with ETL into GCS Flow

[DE Zoomcamp 2.2.5 - Parametrizing Flow & Deployments with ETL into GCS flow](https://www.youtube.com/watch?v=QrDxPjX10iw)

[Transcript](./week2/materials/03_deployments/Readme.md)

[parameterized_flow.py](./week2/materials/03_deployments/docker_deploy.py)

[docker_deploy.py](./week2/materials/03_deployments/docker_deploy.py)

Prefect **Deployment**: yaml file containing parameters for an execution, which could include deployment information (what environment it will run in).


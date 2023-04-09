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

## Introduction to Workflow Orchestration

[Introduction to Workflow Orchestration](https://www.youtube.com/watch?v=8oLs6pzHp68&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=18)

* Governing your data flow in a way that respects coordination rules
* Orchestration tools let you turn code into a workflow that can be scheduled and observed
* Delivery System Analogy
  * Products in Boxes = Tasks in Workflow
  * Order in Cart = Workflow. Do they get delivered all at once, sequentially, independently, parallelization, concurrency and asynch
  * Delivery = Workflow Orchestration. Schedule, scaleable, guaranteed despite issues, observable, secured

## Introduction to Prefect Concepts

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

## ETL with GCP and Prefect
# Docker Reference
Run commands from within directory containing docker-compose.yaml

# Running Containers

```bash
# start up and shut down
docker-compose up -d
docker-compose down
# get status of docker instance
docker ps
docker network ls
```

Run a simple python container interactively
```bash
docker run -it --entrypoint=bash python:3.9
```

# Using Networks
Note that all elements defined in a docker-compose.yaml file automatically run on the same network without explicitly defining a network file.

```bash
# create
docker network create pg-network
# list
docker network ls
# remove
docker network rm pg-network
```

Reference in a docker container

```bash
--nework=pg.network
```

# Create a docker ingestion script

Convert the script to a dockerfile

```dockerfile
FROM python:3.9.1

# We need to install wget to download the csv file
RUN apt-get install wget
# psycopg2 is a postgres db adapter for python: sqlalchemy needs it
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
```

Build and run the script

```bash
# build the docker image [imagename]:[tag]
docker build -t taxi_ingest:v001 .
#  run the image
docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"
```
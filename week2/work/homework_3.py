""" Homework Assignment 3 """
import os
from pathlib import Path
import pandas as pd
from prefect import flow, task, get_run_logger
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
@task(name="extract_from_gcs", log_prints=True)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    local_path = "../data"
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    gcs_block.get_directory(from_path=gcs_path, local_path="f{local_path}")
    logger = get_run_logger()
    logger.info("Local Path: %s/%s", local_path, gcs_path)
    return Path(f"{local_path}/{gcs_path}")


@task()
def write_bq(dframe: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    dframe.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="prefect-sbx-community-eng",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def etl_gcs_to_bq(month: int, year: int, color: str) -> int:
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(color, year, month)
    dframe = pd.read_parquet(path)
    write_bq(dframe)
    return dframe.count()


@flow(log_prints=True)
def etl_parent_flow(months: list[int], year: int, color: str):
    """Loop through parameters provided and load to big query"""
    total_rows = 0

    for month in months:
        rows = etl_gcs_to_bq(month, year, color)
        total_rows += rows

    print("Rows Processed: %s", total_rows)


if __name__ == "__main__":
    etl_parent_flow(months=[2, 3], year=2019, color="yellow")

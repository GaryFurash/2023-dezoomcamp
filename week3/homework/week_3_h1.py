"""
Pre-reqs:
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of bucket
"""

import io
import os
import gzip
import requests
import pandas as pd
import pyarrow
import logging
import tempfile
from google.cloud import storage


class Constants:
    source_url = ""
    source_service = ""
    gcp_bucket = ""


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # # (Ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, run_constants):
    for i in range(12):

        # set the base file name
        month = '0'+str(i+1)
        month = month[-2:]
        dataset_file = f"{run_constants.source_service}_tripdata_{year}-{month}"

        # fetch the dataset from the web with pandas
        dataset_url = f"{run_constants.source_url}/{run_constants.source_service}/{dataset_file}.csv.gz"
        print(f"Feching URL: {dataset_url}")
        req = requests.get(dataset_url)
        # gz = gzip.GzipFile(StringIO.StringIO(req.content))
        # df = pd.read_csv(gz, compression="gzip")
        # print(df.head(2))
        # print(f"columns: {df.dtypes}")
        # print(f"rows: {len(df)}")

        # local_path = os.path.join(tempfile.gettempdir(), file_name)
        # pd.DataFrame(io.StringIO(r.text)).to_csv(local_path)
        # print(f"Local: {file_name}")
#
        # read it back into a parquet file
        # df = pd.read_csv(local_path)
        # file_name = file_name.replace('.csv.gz', '.parquet')
        # df.to_parquet(file_name, engine='pyarrow', compression="gzip")
        # print(f"Parquet: {file_name}")
        # upload it to gcs
        # upload_to_gcs(bucket, f"data/{service}/{file_name}", local_path)
        # print(f"GCS: {service}/{file_name}")


def main():
    """
    Main Method
    """
    run_constants = Constants()
    run_constants.source_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
    run_constants.source_service = "flv"
    run_constants.gcp_bucket = os.environ.get("GCP_GCS_BUCKET")

    web_to_gcs('2019', run_constants)


if __name__ == "__main__":
    main()

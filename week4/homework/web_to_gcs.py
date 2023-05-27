"""
pre-reqs:
1. `pip install pandas pyarrow google-cloud-storage`
2. set google_application_credentials to your project/service-account key
3. set gcp_gcs_bucket as your bucket or change default value of bucket
"""

# import io
import os
import requests
import pandas as pd
from google.cloud import storage

# services = ['fhv','green','yellow']
init_url = 'https://github.com/datatalksclub/nyc-tlc-data/releases/download/'
# switch out the bucketname
bucket = os.environ.get("gcp_gcs_bucket", "gffurash-prefect-de-zoomcamp")


def upload_to_gcs(bucket, object_name, local_file):
    """
    ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    # # workaround to prevent timeout for files > 6 mb on 800 kbps upload speed.
    # # (ref: https://github.com/googleapis/python-storage/issues/74)
    # storage.blob._max_multipart_size = 5 * 1024 * 1024  # 5 mb
    # storage.blob._default_chunksize = 5 * 1024 * 1024  # 5 mb

    # client = storage.client()
    client = storage.Client.from_service_account_json(
        '/home/garyf/.creds/gcp/polar-column-380322-e760c6bf1a47.json')
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, service):
    for i in range(12):

        # sets the month part of the file_name string
        month = '0'+str(i+1)
        month = month[-2:]

        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # download it using requests via a pandas df
        request_url = f"{init_url}{service}/{file_name}"
        r = requests.get(request_url)
        open(file_name, 'wb').write(r.content)
        print(f"local: {file_name}")

        # read it back into a parquet file
        df = pd.read_csv(file_name, compression='gzip')
        file_name = file_name.replace('.csv.gz', '.parquet')
        df.to_parquet(file_name, engine='pyarrow')
        print(f"parquet: {file_name}")

        # upload it to gcs
        upload_to_gcs(bucket, f"{service}/{file_name}", file_name)
        print(f"gcs: {service}/{file_name}")


# web_to_gcs('2019', 'green')
# web_to_gcs('2020', 'green')
# web_to_gcs('2019', 'yellow')
# web_to_gcs('2020', 'yellow')
web_to_gcs('2019', 'fhv')

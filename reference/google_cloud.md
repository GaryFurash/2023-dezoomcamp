# Google Cloud

[Google Cloud Console](https://console.cloud.google.com/welcome).

Create a Project. It will generate a "fun" unique name.

## Setup

### Setup the Cloud Account and Service Account

1. Select your project and go to the left menu **IAM & Admin**, then **Service Accounts**.
2. Click on **+ CREATE SERVICE ACCOUNT** located at the top.
3. Enter a name in the the **Service account name** field, then click on **CREATE AND CONTINUE** button.
4. Add roles below and click **DONE**
   *. `Storage Admin`: for creating and managing _buckets_.
   *. `Storage Admin`: for creating and managing _buckets_.
   *. `Storage Object Admin`: for creating and managing _objects_ within the buckets.
   *. `BigQuery Admin`: for managing BigQuery resources and data.
   *. `Viewer` should already be present as a role.
5. Enable APIs
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
5. Right under **Actions**, select **Manage keys**. Then under the **ADD KEY** button, select **Create New Key** and keep
**JSON** as key type.
6. Save the private key file to your computer (example `~/opt/gcp`)

### Install Google Cloud CLI

1. Download [Goggle Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk) for local setup (e.g., ~/opt/google-cloud-sdk)
2. From that directory run ```./google-cloud-sdk/install.sh```
3.  Verify the installation by running ```gcloud -v``

## Set Credentials (before using)
This lets you manually set credentials by authenticating with a web page

```bash
$ export GOOGLE_APPLICATION_CREDENTIALS="{path to credentials file}"
$ gcloud auth application-default login
```

## Python to Google Buckets
(assumes other steps above are complete)

Create a virtual enviornment, then run `pip install pandas pyarrow google-cloud-storage -upgrade`

Setup the environment variables, either by putting in a file and sourcing it

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/home/garyf/.creds/gcp/polar-column-380322-e760c6bf1a47.json"
export GCP_GCS_BUCKET="gffurash-prefect-de-zoomcamp"
```

Or you can directly instantiate the enviornment variables in your python script

```python
import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/garyf/.creds/gcp/polar-column-380322-e760c6bf1a47.json'
```

Uploading from file to to buckets

```python
from google.cloud import storage

bucket = os.environ.get("GCP_GCS_BUCKET", "gffurash-prefect-de-zoomcamp")

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

upload_to_gcs(bucket, "flv/file.parquet", "file.parquet")
```
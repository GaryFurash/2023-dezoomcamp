"""
scratchpad
pip install --upgrade google-cloud-storage
"""

import os
from google.cloud import storage

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/garyf/.creds/gcp/polar-column-380322-e760c6bf1a47.json'
# client = storage.client()
storage_client = storage.Client.from_service_account_json(
    '/home/garyf/.creds/gcp/polar-column-380322-e760c6bf1a47.json')

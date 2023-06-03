"""
scratchpad
pip install --upgrade google-cloud-storage
"""

# import os
# from google.cloud import storage
#
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/garyf/.creds/gcp/polar-column-380322-e760c6bf1a47.json'
# client = storage.client()
# storage_client = storage.Client.from_service_account_json(
#    '/home/garyf/.creds/gcp/polar-column-380322-e760c6bf1a47.json')

import pandas as pd

df = pd.read_csv('yellow_tripdata_2019-10.csv.gz', compression='gzip')
df.info()
print(df['store_and_fwd_flag'].unique())
df['store_and_fwd_flag'] = df['store_and_fwd_flag'].fillna('')
df['store_and_fwd_flag'] = df['store_and_fwd_flag'].astype('str')
# df['store_and_fwd_flag'] = df['store_and_fwd_flag'].replace(np.nan, '')
# i = 0
# for col_name in df.columns:
#    i = i + 1
#    print(f"{i}: {col_name}")

from dotenv import load_dotenv
from os import getenv, path
import pandas as pd
import requests

# SWAGGER docs
V1_DATA_PREFIX = "api/v1/db/data/v1"

# load the environment variables
load_dotenv()

auth_token = getenv('nocodb_auth_token')
nocodb_base_uri = getenv('nocodb_url')
org_name = getenv('nocodb_org_name')
project_name = getenv('nocodb_project_name')
upload_file_path = getenv('nocodb_upload_file_path')
table_name = getenv('nocodb_table_name')
chunk_size = int(getenv('nocodb_upload_file_chunk_size'))

# authenticate with the api key
headers = {
    'xc-auth': auth_token,
    'accept': 'application/json'
}

# construct the uri for the upload
insert_row_uri = path.join(nocodb_base_uri, V1_DATA_PREFIX, project_name, table_name)

# read the csv file in chunks
for df in pd.read_csv(upload_file_path, chunksize=chunk_size):
    # upload the file one row at a time
    for index, row in df.iterrows():
        # body of json request
        body = row.to_dict()
        body['Id'] = body['index']
        print(body)
        r = requests.post(insert_row_uri, headers=headers, json=body)
        r.raise_for_status()

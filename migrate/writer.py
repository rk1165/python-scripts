import argparse
import configparser
import json

import boto3
import requests
from requests_aws4auth import AWS4Auth
import sqlite3
from multiprocessing.pool import ThreadPool

# need to create separate credentials for different regions
credentials = boto3.Session().get_credentials()

parser = argparse.ArgumentParser(description="Read document from ES in one region and write it to another region's ES")

args = parser.parse_args()

config = configparser.ConfigParser()
config.read('es_config.ini')

from_host = config['from']['host']
from_index = config['from']['index']
from_region = config['from']['region']

from_awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, from_region, 'es',
                        session_token=credentials.token)
headers = {"Content-Type": "application/json"}

'''
1. Read the FRs from database
2. Fetch the data from ES (old)
3. Manipulate the data in memory (if required)
4. Post to S3 and ES (new)

NB: Parallelize on FR
'''


# Fetches the ids of the document to be retrieved
def load_frs_from_db(db):
    con = sqlite3.connect(db)
    cursor = con.cursor()
    cursor.execute("SELECT fr FROM migration_stats")
    rows = cursor.fetchall()
    ids = [row[0] for row in rows]
    con.close()
    return ids


# Find the document from ES and write it to a json file
def search_documents(fr):
    url = f"{from_host}/{from_index}/_search"
    query = {
        'query': {
            "bool": {
                "must": [
                    {
                        "match": {
                            "frn": fr
                        }
                    }
                ]
            }
        },
    }

    r = requests.get(url, auth=from_awsauth, headers=headers, data=json.dumps(query))
    json_response = r.json()
    docs = json_response['hits']['hits']
    doc = docs[0]["_source"]
    with open(fr + '.json', 'w') as f:
        f.write(json.dumps(doc))


def post_to_s3_and_es():
    # Bulk ingest in ES
    pass


frs = load_frs_from_db("2022-01-08")
# print(frs[:])

pool = ThreadPool(processes=8)
pool.map(search_documents, frs)

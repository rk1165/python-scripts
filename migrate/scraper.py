import argparse
import configparser
import json
import sqlite3
from ast import literal_eval as make_tuple

import boto3
import curlify
import requests
from requests_aws4auth import AWS4Auth

credentials = boto3.Session().get_credentials()

parser = argparse.ArgumentParser(description="Find daily counts between a start and end date of a query in AWS ES")

args = parser.parse_args()

config = configparser.ConfigParser()
config.read('es_config.ini')

host = config['from']['host']
index = config['from']['index']
region = config['from']['region']

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
headers = {"Content-Type": "application/json"}


def search_documents(start_date, end_date, fr, rows):
    url = host + '/' + index + '/_search'
    query = {
        'query': {
            "bool": {
                "filter": {
                    "range": {
                        "creationDate": {
                            # "format": "yyyy-MM-dd'T'HH:mm:ssZ",
                            "gte": start_date,
                            "lte": end_date
                        }
                    }
                },
                "must_not": [
                    {
                        "match": {
                            # field on which to not match
                            "$FIELD": "$VALUE"
                        }
                    }
                ]
            }
        },
        "_source": [
            # "the field you want",
            "$FIELD_YOU_WANT_FROM_THE_DOCUMENT"
        ],
        "sort": [
            {
                # sorted on the field so that we can search based on anchor
                "$FIELD_TO_SORT_ON": {"order": "asc"}
            }
        ],
        "search_after": [
            # the anchor after which we want to get the field
            fr
        ],
        'size': 10000,
        "track_total_hits": False
    }

    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    print(curlify.to_curl(r.request))
    json_response = r.json()
    # print(json_response)
    docs = json_response['hits']['hits']

    fr_n = ''
    for doc in docs:
        fr_n = doc['_id']
        rows.append((fr_n,))
    # returns the last fr fetched from ES so that in next iteration it fetches after that
    return fr_n


def timely_search(stats):
    start_date, end_date, count = stats
    fr = ''
    con = sqlite3.connect("{}.db".format(start_date[:start_date.index('T')]))
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE migration_stats (fr text)''')
    # total number of iterations to run based on the count of daily document size
    loops = (count // 10000) + 1
    for i in range(loops):
        rows = list()
        fr = search_documents(start_date, end_date, fr, rows)
        cursor.executemany('''INSERT INTO migration_stats values (?)''', rows)
    con.commit()
    con.close()


if __name__ == '__main__':
    total = list()
    with open('total_counts.txt', 'r') as f:
        for line in f.readlines():
            total.append(make_tuple(line.strip('\n')))
    for elem in total:
        timely_search(elem)

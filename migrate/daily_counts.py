import argparse
import configparser
import json
from multiprocessing.pool import ThreadPool

import boto3
import pandas as pd
import requests
from requests_aws4auth import AWS4Auth

credentials = boto3.Session().get_credentials()

parser = argparse.ArgumentParser(description="Find daily counts between a start and end date of a query in AWS ES")
parser.add_argument('sd', help="Start date")
parser.add_argument('ed', help="End date")

args = parser.parse_args()

config = configparser.ConfigParser()
config.read('es_config.ini')

host = config['from']['host']
index = config['from']['index']
region = config['from']['region']

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, 'es', session_token=credentials.token)
headers = {"Content-Type": "application/json"}


def count_documents(start_date, end_date):
    url = host + '/' + index + '/_count'
    query = {
        'query': {
            "bool": {
                "filter": {
                    "range": {
                        "creationDate": {
                            "gte": start_date,
                            "lt": end_date
                        }
                    }
                },
                "must_not": [
                    {
                        "match": {
                            "$FIELD_TO_MATCH": "$VALUE"
                        }
                    }
                ]
            }
        },
    }
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    json_response = r.json()
    # print(json_response)
    return json_response['count']


def generate_time_series(start_date, end_date):
    times = pd.date_range(start=start_date, end=end_date, freq='1D')
    dates = times.to_pydatetime()

    days = []
    for day in dates:
        dt = day.strftime("%Y-%m-%dT%H:%M:%SZ")
        days.append(dt)
    date_pairs = list()
    for i in range(0, len(days) - 1):
        start, end = days[i], days[i + 1]
        date_pairs.append((start, end))
    return date_pairs


result = list()


def time_count(date_pair):
    start_date, end_date = date_pair
    count = count_documents(start_date, end_date)
    result.append((start_date, end_date, count))


time_series = generate_time_series(args.sd, args.ed)

pool = ThreadPool(processes=8)
pool.map(time_count, time_series)

# Sort the result by count
result.sort(key=lambda x: x[0])
print('\n'.join([str(row) for row in result]))

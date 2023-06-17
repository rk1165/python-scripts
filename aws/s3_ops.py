import boto3

s3 = boto3.client('s3')


def list_buckets():
    """
    List existing buckets for an account
    :return:
    """
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f' {bucket["Name"]}')


def list_objects(bucket, prefix=''):
    """
    List all the objects in a bucket with a given prefix. Default value of prefix is empty
    :param bucket: name of the bucket from which to list all objects
    :param prefix: optional parameter to narrow down the path
    :return:
    """
    response = s3.list_objects(Bucket=bucket, Prefix=prefix)
    contents = response['Contents']
    # print(contents)
    for content in contents:
        # print(content)
        print(content['Key'])


def get_object(bucket, key, version=''):
    """
    Get object contents in a bucket
    :param bucket: name of the bucket from which to get the object
    :param key: name of the key - like file name
    :param version: optional parameter to retrieve a specific version
    :return:
    """
    response = s3.get_object(Bucket=bucket, Key=key, VersionId=version)
    print(response)
    content = response['Body'].read().decode('utf-8')
    print(content)


def get_all_versions(bucket, prefix):
    """
    Get all versions of a file in S3
    :param bucket: name of the bucket
    :param prefix: name of the file whose versions to see
    :return:
    """
    response = s3.list_object_versions(Bucket=bucket, Prefix=prefix)
    print(response)
    versions = response['Versions']
    for version in versions:
        version_id = version['VersionId']
        key = version['Key']
        get_object(bucket, key, version_id)


list_buckets()
list_objects('fulfillment-repo')
list_objects('fulfillment-repo', 'fulfillment/ds17')
get_object('fulfillment-repo', 'fulfillment/ds17/file1.js')
get_all_versions('fulfillment-repo', 'fulfillment/ds17/file1.js')

import argparse
from collections import defaultdict

import boto3

parser = argparse.ArgumentParser(description='Retrieve basic information from the running EC2')
parser.add_argument('region')
args = parser.parse_args()

# Connect to EC2
ec2 = boto3.resource('ec2', args.region)


def get_instances():
    """Get all running EC2 instances"""
    running_instances = ec2.instances.filter(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ])
    return running_instances


def get_ec2_info():
    """Get Info about the running EC2 instances"""
    ec2info = defaultdict()
    running_instances = get_instances()
    for instance in running_instances:
        name = ''
        for tag in instance.tags:
            if 'Name' in tag['Key']:
                name = tag['Value']
        # Add instance info to a dictionary
        ec2info[instance.id] = {
            'Name': name,
            'Type': instance.instance_type,
            'State': instance.state['Name'],
            'Private IP': instance.private_ip_address,
            'Public IP': instance.public_ip_address,
            'Launch Time': instance.launch_time
        }

    attributes = ['Name', 'Type', 'State', 'Private IP', 'Public IP', 'Launch Time']
    for instance_id, instance in ec2info.items():
        for key in attributes:
            print(f"{key:<12}: {instance[key]}")
        print("-------------------------------")

get_ec2_info()
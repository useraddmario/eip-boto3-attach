#!/usr/bin/env python3

import boto3
import json
import pprint
from botocore.exceptions import ClientError


pp = pprint.PrettyPrinter(indent=4)
SEARCHTERM = 'Jump'

####Get Jump EIP AllocationId####
ec2 = boto3.client('ec2')
filters = [
    {'Name': 'domain', 'Values': ['vpc']}
]
response = ec2.describe_addresses(Filters=filters)

#Iterate for SEARCHTERM and save 'AllocationId'
allocid = ''
for address in response['Addresses']:
    for each in address['Tags']:
        if SEARCHTERM in each['Value']:
            allocid = address['AllocationId']

print(allocid)
print('\n###########################\n')


####Get correct ASG####
asg = boto3.client('autoscaling')
response = asg.describe_auto_scaling_groups()

#Iterate for SEARCHTERM and save 'InstanceId'
instanceid = ''
for group in response['AutoScalingGroups']:
    if SEARCHTERM in group['AutoScalingGroupName']:
        instanceid = group['Instances'][0]['InstanceId']

pp.pprint(instanceid)
print('\n###########################\n')



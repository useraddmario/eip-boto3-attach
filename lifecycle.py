#!/usr/bin/env python3

import boto3
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)


####Get Jump EIP AllocationId####
ec2 = boto3.client('ec2')
filters = [
    {'Name': 'domain', 'Values': ['vpc']}
]
response = ec2.describe_addresses(Filters=filters)

allocid = ''
#Iterate for 'JumpEIP' and save 'AllocationId'
for address in response['Addresses']:
    for each in address['Tags']:
        if each['Value'] == 'JumpEIP':
            allocid = address['AllocationId']

print(allocid)
print('\n###########################\n')


####Get correct ASG####
asg = boto3.client('autoscaling')

response = asg.describe_auto_scaling_groups(
    AutoScalingGroupNames=[
        'string',
    ],
    NextToken='string',
    MaxRecords=123
)
pp.pprint(response)

#for group in response[

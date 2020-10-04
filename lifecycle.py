#!/usr/bin/env python3

import boto3
import json
import pprint
import logging
from botocore.exceptions import ClientError
import subprocess

pp = pprint.PrettyPrinter(indent=4)
SEARCHTERM = 'Jump'

####Generate a log filr####
subprocess.run(["touch", "boto3-init.log"])

####Add logging####
logging.basicConfig(
    filename='boto3-init.log',
    level=logging.INFO,
    format=f'%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger()
logger.debug('The script is starting.')
logger.info('Connecting to EC2...')

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

logger.info(allocid)


####Get Jump ASG####
asg = boto3.client('autoscaling')
response = asg.describe_auto_scaling_groups()

#Iterate for SEARCHTERM and save 'InstanceId'
instanceid = ''
for group in response['AutoScalingGroups']:
    if SEARCHTERM in group['AutoScalingGroupName']:
        instanceid = group['Instances'][0]['InstanceId']

logger.info(instanceid)


####Associate EIP with Jump Box####

try:
    response = ec2.associate_address(AllocationId=allocid,
                                     InstanceId=instanceid)
    logger.info(response)
except ClientError as e:
    logger.info(e)




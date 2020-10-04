#!/usr/bin/env python3

import boto3
import logging
from botocore.exceptions import ClientError
import subprocess
import pprint
import json

pp = pprint.PrettyPrinter(indent=4)
SEARCHTERM = 'Jump'
ec2 = boto3.client('ec2')
asg = boto3.client('autoscaling')

####Init logging####
LOG = 'boto3-init.log'
logging.basicConfig(
        filename='boto3-init.log',
        level=logging.INFO,
        format=f'%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger()

####Generate a log file####
subprocess.run(["touch", "boto3-init.log"])


def parse_jump_eip():
    ####Get Jump EIP AllocationId####
    logger.info('Parsing EIP...')

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
    logger.info('The jump EIP is ' + allocid)
    return allocid

def parse_jump_asg():
    ####Get Jump ASG####
    logger.info('Parsing ASG...')
    
    response = asg.describe_auto_scaling_groups()

    #Iterate for SEARCHTERM and save 'InstanceId'
    instanceid = ''
    for group in response['AutoScalingGroups']:
        if SEARCHTERM in group['AutoScalingGroupName']:
            instanceid = group['Instances'][0]['InstanceId']
    logger.info('The jump ASG is ' + instanceid)
    return instanceid

def eip_associate(allocid, instanceid):
    ####Associate EIP with Jump Box####
    logger.info('Associating EIP...')
    
    try:
        response = ec2.associate_address(AllocationId=allocid,
                                     InstanceId=instanceid)
        logger.info(response)
        return response
    except ClientError as e:
        logger.info(e)

def main():
    allocid = parse_jump_eip()
    instanceid = parse_jump_asg()
    response = eip_associate(allocid, instanceid)
    print(response['AssociationId'])


if __name__ == '__main__':
    main()









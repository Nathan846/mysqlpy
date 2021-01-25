# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 13:36:53 2021

@author: Vaidhyanathan C
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 12:29:06 2021

@author: Vaidhyanathan C
"""
import boto3
import time
import os
region = 'ap-south-1'
buckname = 'buckvaidhyanathan'
logname = 'CloudWatch-Logs'
streamname = 'Boto3stream'
logs = boto3.client('logs',region_name=region)
try:
    response = logs.create_log_group(
    logGroupName=logname)
except logs.exceptions.ResourceAlreadyExistsException:
    print('LogGroup Already Present')
try:
    logs.create_log_stream(logGroupName=logname,logStreamName=streamname)
except logs.exceptions.ResourceAlreadyExistsException:
    print('Stream is already present')
t = logs.describe_log_streams(logGroupName=logname,logStreamNamePrefix=streamname)
token = t['logStreams'][0]['uploadSequenceToken']
resp = logs.put_log_events(logGroupName='CloudWatch-Logs',
    logStreamName='Boto3stream',
    logEvents=[
        {
            'timestamp': int(round(time.time() * 1000)),
            'message': 'Written from EC2_User_data'
        }],
        sequenceToken = token
    )
try:
    token = resp['nextSequenceToken']
    print('Log Event successfully written.')
except KeyError:
    print('Unable to process the request')

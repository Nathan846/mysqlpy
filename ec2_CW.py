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
streamname = 'Stream'
logs = boto3.client('logs',region_name=region)
try:
    response = logs.create_log_group(
    logGroupName=logname)
except logs.exceptions.ResourceAlreadyExistsException:
    print('LogGroup Already Present')
try:
    os.environ['seqtoken']
except:
    os.environ['seqtoken'] = str(5)
try:
    logs.create_log_stream(logGroupName=logname,logStreamName=streamname)
except logs.exceptions.ResourceAlreadyExistsException:
    print('Stream is already present')
resp = logs.put_log_events(logGroupName='CloudWatch-Logs',
    logStreamName='Boto3stream',
    logEvents=[
        {
            'timestamp': int(round(time.time() * 1000)),
            'message': 'Written from EC2_User_data'
        }],
        sequenceToken = os.environ['seqtoken']
    )
try:
    os.environ['seqtoken'] = resp['nextSequenceToken']
    print('Log Event successfully written.')
    print('Sequence token saved as an environment variable for the next put event.')
except KeyError:
    print('Unable to process the request')

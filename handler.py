import boto3
import urllib3
import json
import os
import logging
import sys


sqs = boto3.client('sqs')
s3 = boto3.client("s3")

def lambda_handler(event, context):
    # SQS url from serverless variable
    sqs_url = os.environ['QUEUE_URL']
    print("SQS-url: ", sqs_url)
    
    # Bucket name from serverless variable 
    bucketname  = os.environ['S3']
    print("Bucket-name: ", bucketname)

    #Get file name
    filename = str(event["Records"][0]['s3']['object']['key'])
    print("File-name: ", filename)

    #Get data from file object
    fileObj = s3.get_object(Bucket=bucketname, Key=filename)
    data = fileObj["Body"].read().decode('utf-8')
    jstr = json.dumps(data, indent=4)
    print(jstr)

    # Push data to sqs  
    response = sqs.send_message(QueueUrl=sqs_url,    DelaySeconds=10,    MessageBody=(jstr))
    
    return {'status_code': 200}
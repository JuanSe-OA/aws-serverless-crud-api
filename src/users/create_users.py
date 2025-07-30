import json
import boto3
import os
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.environ['USERS_TABLE'])

def handler(event, context):
    body = json.loads(event['body'])
    user_id = str(uuid.uuid4())
    
    item = {
        'userId': user_id,
        'name': body.get('name'),
        'email': body.get('email')
    }

    table.put_item(Item=item)

    return {
        "statusCode": 201,
        "body": json.dumps({"message": "User created", "userId": user_id})
    }

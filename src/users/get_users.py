import json
import boto3
import os
from boto3.dynamodb.conditions import Key
# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1',endpoint_url='http://localhost:8000',
)
table = dynamodb.Table('usersTable')

def handler(event, context):
    response = {
        "statusCode": 200,
        "body": ''
    }

    params = {
        'KeyConditionExpression': Key('pk').eq('1')
    }

    try:
        # Ejecutar la consulta
        res = table.query(
            KeyConditionExpression=params['KeyConditionExpression']
        )
        print(res)
        response['statusCode'] = 200
        response['body'] = json.dumps({'users': res.get('Items', [])})

    except Exception as e:
        print(f"Error querying DynamoDB: {e}")
        response['statusCode'] = 500
        response['body'] = json.dumps({'error': str(e)})

    return response
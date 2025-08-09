import json
import boto3
import os
from boto3.dynamodb.conditions import Key

# Configuración para DynamoDB local u online
dynamodb_client_params = {}
if os.environ.get('IS_OFFLINE'):
    dynamodb_client_params = {
        'region_name': 'localhost',
        'endpoint_url': 'http://localhost:8000',

    }

dynamodb = boto3.resource('dynamodb', **dynamodb_client_params)
table = dynamodb.Table('usersTable')

def get_user(event, context):
    response = {
        "statusCode": 200,
        "body": ''
    }

    try:
        user_id = event['pathParameters']['id']  # Obtener el ID del path

        res = table.query(
            KeyConditionExpression=Key('pk').eq(user_id)
        )

        response['body'] = json.dumps(res.get('Items', []))

    except Exception as e:
        print(f"Error querying DynamoDB: {e}")
        response['statusCode'] = 500
        response['body'] = json.dumps({'error': str(e)})

    return response

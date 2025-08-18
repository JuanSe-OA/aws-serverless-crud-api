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
table = dynamodb.Table(os.environ['TABLE_NAME'])

def update_user(event, context):
    response = {
        "statusCode": 200,
        "body": ''
    }

    try:
        user_id = event['pathParameters']['id']  
        body = json.loads(event['body'])  

        name = body.get('name')
        email = body.get('email')

        if not name or not email:
            raise ValueError("Both 'name' and 'email' are required")

        res = table.update_item(
            Key={'pk': user_id},
            UpdateExpression="SET #n = :n, email = :e",  
            ExpressionAttributeNames={
                '#n': 'name'
            },
            ExpressionAttributeValues={
                ':n': name,
                ':e': email
            },
            ReturnValues="ALL_NEW"
        )

        response['statusCode'] = 200
        response['body'] = json.dumps({
            'message': 'User updated successfully',
            'user': res.get('Attributes', {})
        })

    except Exception as e:
        print(f"Error updating user: {e}")
        response['statusCode'] = 500
        response['body'] = json.dumps({'error': str(e)})

    return response


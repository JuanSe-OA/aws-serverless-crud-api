import json
import boto3
import os
import uuid
from boto3.dynamodb.conditions import Key



# Configuración para DynamoDB local u online
dynamodb_client_params = {}
if os.environ.get('IS_OFFLINE'):
    dynamodb_client_params = {
        'region_name': 'us-east-1',  # o cualquier región válida
        'endpoint_url': 'http://localhost:8000',
    }

dynamodb = boto3.resource('dynamodb', **dynamodb_client_params)
table = dynamodb.Table(os.environ['TABLE_NAME'])

def create_user(event, context):
    response = {
        "statusCode": 200,
        "body": ""
    }

    try:
        # Extraer y decodificar el cuerpo del request
        body = json.loads(event.get('body', '{}'))

        # Generar un único ID
        user_id =  str(uuid.uuid4())

        # Aquí puedes extraer más campos si los estás guardando (ej: name, email)
        name = body.get('name', 'No Name')
        telefone = body.get('telephone', 'No Telephone')
        email = body.get('email', 'No Email')

        # Construir el ítem
        item = {
            'pk': user_id,
            'name': name,
            'telephone': telefone,
            'email': email
        }

        # Guardar en DynamoDB
        table.put_item(Item=item)

        response['statusCode'] = 201
        response['body'] = json.dumps({
            "message": "User created successfully",
            "user": item
        })

    except Exception as e:
        print(f"Error creating user: {e}")
        response['statusCode'] = 500
        response['body'] = json.dumps({'error': str(e)})

    return response
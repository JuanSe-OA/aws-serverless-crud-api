import boto3
import os
import json
from botocore.config import Config

config = Config(signature_version='s3v4')

s3_client = boto3.client('s3', config=config)

def signeds3_url(event, context):
    # Se obtiene el nombre del archivo de los parámetros de la URL
    filename = event['queryStringParameters']['filename']
    
    # Se define el bucket y la clave del objeto
    bucket_name = os.environ.get('BUCKET')
    object_key = f"upload/{filename}"
    
    # Se genera la URL firmada para la operación 'put_object'
    # 'ExpiresIn' define la validez de la URL en segundos
    signed_url = s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_key,
        },
        ExpiresIn=300
    )
    
    # Se devuelve la URL firmada en la respuesta HTTP
    return {
        'statusCode': 200,
        'body': json.dumps(signed_url),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
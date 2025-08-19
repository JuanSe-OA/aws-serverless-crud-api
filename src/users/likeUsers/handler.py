import boto3
import json
import time

# Cliente de DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("usersTable")

def likeuser(event, context):
    # Obtener el mensaje de SQS
    body = event["Records"][0]["body"]
    user_id = json.loads(body)["id"]
    print(f"User ID recibido: {user_id}")

    # Parámetros para la actualización
    params = {
        "Key": {"pk": user_id},
        "UpdateExpression": "ADD likes :inc",
        "ExpressionAttributeValues": {
            ":inc": 1
        },
        "ReturnValues": "ALL_NEW"
    }

    # Ejecutar la actualización
    result = table.update_item(**params)

    # Esperar 4 segundos (simula sleep en Node)
    time.sleep(4)

    print("Resultado de la actualización:", result)
    return result

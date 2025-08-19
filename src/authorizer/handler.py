from datetime import datetime, UTC

def authorizer(event, context):
    secret = "NuestraVariableSecreta"  # ⚠️ usar AWS SSM o Secrets Manager en prod
    current_time = datetime.now(UTC)   # reemplazo de utcnow()
    hour = current_time.hour
    minute = current_time.minute

    token = event.get("authorizationToken")
    valid_token = f"Bidder {secret}{hour}{minute}"

    if token == valid_token:
        return {
            "principalId": "user",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": "*"
                    }
                ]
            }
        }
    else:
        raise Exception("Unauthorized")
        return {
            "statusCode": 401,
            "body": "Unauthorized"
        }
    

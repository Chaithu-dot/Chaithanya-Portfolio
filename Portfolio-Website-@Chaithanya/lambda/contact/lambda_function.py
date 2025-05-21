import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ContactFormSubmission')

def lambda_handler(event, context):
    try:
        # Debug logs
        print("=== RAW EVENT ===")
        print(json.dumps(event))

        body = json.loads(event.get('body', '{}'))  # Safe parse

        print("=== PARSED BODY ===")
        print(json.dumps(body))

        item = {
            'id': str(uuid.uuid4()),
            'name': body.get('name', 'MISSING'),
            'email': body.get('email', 'MISSING'),
            'phone': body.get('phone', 'MISSING'),
            'message': body.get('message', 'MISSING'),
            'timestamp': datetime.utcnow().isoformat()
        }

        print("=== FINAL ITEM ===")
        print(json.dumps(item))

        # Insert into DynamoDB
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Form submitted successfully'})
        }

    except Exception as e:
        print("=== ERROR ===")
        print(str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

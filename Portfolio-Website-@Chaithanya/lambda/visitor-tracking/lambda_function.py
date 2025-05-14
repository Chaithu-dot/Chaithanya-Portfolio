import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')
table = dynamodb.Table('VisitorLogs')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))

        page = body.get('page', '/')
        user_agent = body.get('userAgent', '')
        referrer = body.get('referrer', '')
        timestamp = datetime.utcnow().isoformat()

        item = {
            'id': str(uuid.uuid4()),
            'timestamp': timestamp,
            'page': page,
            'userAgent': user_agent,
            'referrer': referrer
        }

        table.put_item(Item=item)

        cloudwatch.put_metric_data(
            Namespace='VisitorAnalytics',
            MetricData=[
                {
                    'MetricName': 'PageView',
                    'Dimensions': [
                        {
                            'Name': 'Page',
                            'Value': page
                        }
                    ],
                    'Unit': 'Count',
                    'Value': 1
                }
            ]
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Visitor logged'})
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

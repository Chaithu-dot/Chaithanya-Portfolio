import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')
table = dynamodb.Table('ContactTracking')

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

        # Save visitor data
        table.put_item(Item=item)

        # Push CloudWatch metric
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
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Visitor logged'})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

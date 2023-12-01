import os
import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE_NAME']
table = dynamodb.Table(table_name)
s3_bucket_name = os.environ['S3_BUCKET_NAME']

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])
        total_items = len(items)
        date_today = datetime.now().strftime('%Y%m%d')
        filename = f'{date_today}.txt'
        file_content = {'total_items': total_items}
        s3_client = boto3.client('s3')
        s3_client.put_object(Body=json.dumps(file_content), Bucket=s3_bucket_name, Key=filename)
        return {
            'statusCode': 200,
            'body': json.dumps({'total_items': total_items, 'filename': filename})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Something went wrong: {str(e)}')
        }
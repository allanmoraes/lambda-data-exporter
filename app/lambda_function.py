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
        # Realiza a varredura (scan) na tabela DynamoDB
        response = table.scan()

        # Verifica se a varredura foi bem-sucedida
        items = response.get('Items', [])
        
        # Conta o número total de itens
        total_items = len(items)

        # Obtém a data atual no formato YYYYMMDD
        date_today = datetime.now().strftime('%Y%m%d')

        # Nome do arquivo no formato YYYYMMDD.txt
        filename = f'{date_today}.txt'

        # Conteúdo do arquivo
        file_content = {'total_items': total_items}

        # Salvando o conteúdo no S3
        s3_client = boto3.client('s3')
        s3_client.put_object(Body=json.dumps(file_content), Bucket=s3_bucket_name, Key=filename)

        return {
            'statusCode': 200,
            'body': json.dumps({'total_items': total_items, 'filename': filename})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Ocorreu um erro: {str(e)}')
        }
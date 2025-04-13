import json
import boto3

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('NewsArticles')

        response = table.scan()
        articles = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(articles)
        }

    except Exception as e:
        print(f"Error reading from DynamoDB: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }

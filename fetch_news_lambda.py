import json
import boto3
import urllib3
import uuid
from datetime import datetime

http = urllib3.PoolManager()

def lambda_handler(event, context):
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('NewsArticles')

        # ✅ Use working API — try GNews (adjust your API key here)
        url = f'https://gnews.io/api/v4/top-headlines?token=YOUR_GNEWS_API_KEY&lang=en'

        response = http.request('GET', url)
        data = json.loads(response.data.decode('utf-8'))

        print(f"Fetched {len(data.get('articles', []))} articles")

        for article in data.get('articles', []):
            try:
                table.put_item(
                    Item={
                        'articleId': str(uuid.uuid4()),
                        'title': article.get('title', 'No Title'),
                        'description': article.get('description', 'No Description'),
                        'url': article.get('url', 'No URL'),
                        'publishedAt': article.get('publishedAt', 'No Date'),
                        'source': article['source']['name'] if article.get('source') else 'No Source',
                        'timestamp': datetime.utcnow().isoformat()
                    }
                )
                print(f"Inserted article: {article.get('title', 'No Title')}")
            except Exception as e:
                print(f"Error inserting article into DynamoDB: {e}")

        return {
            'statusCode': 200,
            'body': json.dumps('News articles stored successfully!')
        }

    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }

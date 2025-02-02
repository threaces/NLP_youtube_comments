import boto3
import os
from dotenv import load_dotenv
from get_data import prepare_comments_saving

load_dotenv()

access_key = os.getenv('aws_access_key')
secret_key = os.getenv('aws_secret_key')

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name='eu-north-1')

table = dynamodb.Table('Arsenal_comments')

list_of_comments = prepare_comments_saving()

counter = 1

for item in list_of_comments:
    table.put_item(Item={'index_number': counter,
                         'Comment': item['Comment'],
                         'Likes': item['Likes'],
                         'Date': item['Date'],
                         'Match': item['Match']})
    counter += 1



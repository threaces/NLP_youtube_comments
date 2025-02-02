from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import boto3
import pandas as pd


def connect_to_boto(aws_key:str, aws_secret_key:str):

    """
    Function to connect with aws s3 client.
    Args:
        aws_key (str); access key to aws account
        aws_secret_key (str); access secret key to aws account
    Returns:
        boto_object; Boto3 object
    """

    boto_object = boto3.client('s3',
                               aws_access_key_id=aws_key,
                               aws_secret_access_key=aws_secret_key)
    
    return boto_object

def read_video_data(aws_client, bucket_name:str):

    """
    Function to get and read a data from csv file,
    Args:
        aws_client; created aws object
        bucket_name (str); user bucket name
    """

    response = aws_client.list_objects_v2(Bucket=bucket_name)
    list_of_files = response['Contents']        
    latest_file = max(list_of_files, key=lambda x: x['LastModified'])

    csv_object = aws_client.get_object(Bucket='pl-video-id', Key=latest_file['Key'])
    df = pd.read_csv(csv_object['Body'])
    
    return df

def get_content(yt_api_key: str, video_id: str) -> dict:

    """
    Function to get raw content from youtube video.
    Args:
        yt_api_key (str); Unique user api key for youtube developer app
        video_id (str); Id collected from video url
    Returns:
        request (dict); Raw content
    """
    
    youtube = build('youtube', 'v3', developerKey=yt_api_key)
    request = youtube.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100, order='relevance').execute()

    return request

def get_comments(page_content:dict, teams_name:str) -> list[dict]: 
    
    """
    This function processes a dataset containing comments and their replies (such as from a YouTube comment API response) 
    and extracts relevant information about each comment into a structured format. Each comment, including replies if available, 
    is represented as a dictionary containing its text, the number of likes, and the publication date.

    Args:
        page_content (dict): A dictionary containing comment data, typically structured with items, snippets, and replies.
    Returns:
        list_of_dict (list): A list of dictionaries where each dictionary represents a comment or reply. 
                             Each dictionary includes the following keys:
        Comment (str): The text of the comment.
        Likes (int): The number of likes the comment has received.
        Date (str): The publication date of the comment in ISO 8601 format.
    """

    list_of_dict = []

    for item in page_content['items']:

        if item['snippet']['totalReplyCount'] > 0:
            for reply in item['replies']['comments']:

                dict_with_data = {}

                reply = reply['snippet']
                
                comment = str(reply['textDisplay'])
                likes_count = int(reply['likeCount'])
                publishe_date = reply['publishedAt']

                dict_with_data['Comment'] = comment
                dict_with_data['Likes'] = likes_count
                dict_with_data['Date'] = publishe_date
                dict_with_data['Match'] = teams_name

                list_of_dict.append(dict_with_data)
        else:
            dict_with_data = {}
            raw_data = item['snippet']['topLevelComment']['snippet']

            comment = str(raw_data['textDisplay'])
            likes_count = int(raw_data['likeCount'])
            publishe_date = raw_data['publishedAt']

            dict_with_data['Comment'] = comment
            dict_with_data['Likes'] = likes_count
            dict_with_data['Date'] = publishe_date
            dict_with_data['Match'] = teams_name

            list_of_dict.append(dict_with_data)

    return list_of_dict

def prepare_comments_saving():

    """
    Main processing script for fetching, processing, and assigning unique identifiers to YouTube video comments.
    Steps:
    1. Load the YouTube API key from environment variables.
    2. Iterate through a dictionary of video IDs (`dict_of_id`) and fetch raw video content.
    3. Extract comments from the fetched video data.
    4. Assign unique IDs to each comment and structure the data for further use.

    Key Variables:
    - dict_of_id (dict): A nested dictionary containing video IDs and match-related metadata.
    - list_of_contents (list): Stores tuples of raw video data and associated match identifiers.
    - list_of_data (list): Contains the comments extracted for each video and match pair.
    - list_of_modified_data (list): Processed comments with unique identifiers added.
    - counter (int): A sequential counter used to assign unique IDs to comments.

    Returns:
        list_of_modified_data (list): A structured list of processed comments, each with a unique identifier.
    """

    load_dotenv()

    api_key = os.getenv('Youtube_api')

    list_of_contents = []
    list_of_data = []

    list_of_modified_data = []

    for item in dict_of_id.keys():
        
        matches = dict_of_id[item].keys()

        for match in matches:
            video_id = dict_of_id[item][match]['video_id']
            raw_data = get_content(api_key, video_id)
            list_of_contents.append((raw_data, match))

    for item in list_of_contents:
        match_comments = get_comments(item[0], item[1])
        list_of_data.append(match_comments)

    counter = 0

    for item in list_of_data:
        for match_data in item:
            counter += 1
            match_data['Id'] = counter
            list_of_modified_data.append(match_data)

    return list_of_modified_data

load_dotenv()
access_key = os.getenv('aws_access_key')
secret_key = os.getenv('aws_secret_key')
s3_client = connect_to_boto(access_key, secret_key)
read_video_data(s3_client, 'pl-video-id')
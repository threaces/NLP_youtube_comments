import pandas as pd

def get_football_competition(video_id: str, 
                             video_details:dict, 
                             yt_client, 
                             list_of_competition:list) -> dict:

    request = yt_client.videos().list(part='snippet,statistics', id=video_id)
    response = request.execute()
    video_description = response['items'][0]['snippet']['description']

    competition_extract = next((competition for competition in list_of_competition if competition in video_description), None)

    if competition_extract:
        video_details['Competition'] = competition_extract

    return video_details

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

def get_content(yt_object, video_id: str) -> dict:

    """
    Function to get raw content from youtube video.
    Args:
        yt_object (str); yt object created after connecting with api
        video_id (str); Id collected from video url
    Returns:
        request (dict); Raw content
    """
    
    request = yt_object.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100, order='relevance').execute()

    return request
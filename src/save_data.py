import pandas as pd
import io
import scrapetube
import os
from dotenv import load_dotenv
from datetime import datetime
from src.transform_data import transform_data_input
from src.get_data import get_football_competition
from src.connect_to_client import connect_to_yt
from support_elements import football_competition

load_dotenv()

api_key = os.getenv('Youtube_api')
yt_client = connect_to_yt(api_key)


def save_data_to_s3(df:pd.DataFrame, aws_client, s3_bucket_name:str):

    """
    Function to convert pandas dataframe into csv and save csv file into S3 bucket.

    Args:
        df (pd.Dataframe); Dataframe with data related to video (id, teams, date)
        aws_client; Client to connect with aws
        s3_bucket_name (str); Location where user wants to store csv file
    """

    with io.StringIO() as csv_buffer:
        df.to_csv(csv_buffer, index=False)

        filename = datetime.now().strftime('Big6_video_id-%Y-%m-%d.csv')

        response = aws_client.put_object(
            Bucket=s3_bucket_name,
            Key=filename,
            Body=csv_buffer.getvalue()
        )

        return response
    
def saving_to_dataframe(yt_playlist:list) -> pd.DataFrame:

    """
    Function to save all of data from youtube playlist into dataframe

    Args:
        yt_playlist (list[str]); List with playlists id
    Returns:
        df (pd.Dataframe); Dataframe with information about football matches
    """

    list_of_api_data = []

    for playlist in yt_playlist:
        req = scrapetube.get_playlist(playlist_id=playlist)
        list_of_api_data.append(req)

    list_of_data = []

    for item in list_of_api_data:
        club_data = transform_data_input(item)
        list_of_data.append(club_data)

    video_information = []

    for club_playlist in list_of_data:
        for video in club_playlist:
            video_information.append(get_football_competition(video['video_id'], video, yt_client, football_competition))

    df = pd.DataFrame(video_information)

    return df

import os
from dotenv import load_dotenv
from src.connect_to_client import connect_to_boto
from src.save_data import saving_to_dataframe, save_data_to_s3
from support_elements import list_of_playlist_id


if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('Youtube_api')
    access_key = os.getenv('aws_access_key')
    secret_key = os.getenv('aws_secret_key')
    aws_client = connect_to_boto(access_key, secret_key)

    df = saving_to_dataframe(list_of_playlist_id)
    save_data_to_s3(df, aws_client, 'pl-video-id')

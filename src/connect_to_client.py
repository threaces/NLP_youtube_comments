import boto3
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    
def connect_to_yt(yt_api_key:str):
        
    """
    Function to connect with youtube api.
    Args:
        yt_api_key (str); Unique user key for api connection
    Returns:
        yotubue; youtube object
    """
    try:
        youtube = build('youtube', 'v3', developerKey=yt_api_key)

        return youtube
    except HttpError as e:

        return {'error': f"HTTP Error {e.resp.status}: {e.content}"}
    
def connect_to_database(db_name:str,
                        db_password:str,
                        db_user:str,
                        db_host:str):

    """
    Function to connect with database.
    Args:
        db_name (str); database name
        db_passowrd (str); database password
        db_user (str); user login name
        db_host (str); host name
    Returns:
        session; database connection object
    """

    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}')
    Session = sessionmaker(bind=engine)

    return engine, Session
from dotenv import load_dotenv
from src.connect_to_client import connect_to_boto
from src.save_data import saving_to_dataframe, save_data_to_s3
from support_elements import list_of_playlist_id

import os
import logging

"""
Function to run the pipeline responsible for 
collecting id of youtube video from youtube playlist and save into
csv file which is stored in S3 bucket
"""

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('video_id_pipeline.log')
    ]
)

logger = logging.getLogger()


if __name__ == "__main__":
    
    try:
        load_dotenv()
        api_key = os.getenv('Youtube_api')
        access_key = os.getenv('aws_access_key')
        secret_key = os.getenv('aws_secret_key')

        logger.info("Connecting to AWS...")
        aws_client = connect_to_boto(access_key, secret_key)
        logger.info("AWS connection successful.")

        logger.info("Saving preparation...")
        df = saving_to_dataframe(list_of_playlist_id)
        logger.info("Video id saved into dataframe")

        logger.info("Converting dataframe into csv and sending to S3 bucket")
        save_data_to_s3(df, aws_client, 'pl-video-id')
        logger.info("Process completed")

    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

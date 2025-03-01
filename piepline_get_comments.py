from src.connect_to_client import connect_to_yt
from dotenv import load_dotenv

import os


if __name__ == "__main__":

    load_dotenv()

    yt_api_key = os.getenv('Youtube_api')
    connect_to_yt()
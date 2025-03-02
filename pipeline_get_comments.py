from src.connect_to_client import connect_to_yt, connect_to_boto
from src.get_data import read_video_data
from src.transform_data import prepare_comments_saving
from dotenv import load_dotenv
from src.connect_to_client import connect_to_database
from database.models.database_tables import RawComments, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import pprint

if __name__ == "__main__":

    load_dotenv()

    yt_api_key = os.getenv('Youtube_api')
    access_key = os.getenv('aws_access_key')
    secret_key = os.getenv('aws_secret_key')
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    hostname = os.getenv('DB_HOST')
    database_name = os.getenv('DB_NAME')

    yt_client = connect_to_yt(yt_api_key)
    aws_client = connect_to_boto(access_key, secret_key)

    video_id_table = read_video_data(aws_client, 'pl-video-id')

    comments = prepare_comments_saving(yt_client, video_id_table)

    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{hostname}/{database_name}')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    with Session() as session:
        exisiting_comments = {row.comment for row in session.query(RawComments.comment).all()}

        new_comments = [RawComments(comment=data['Comment'], id=data['Id'], likes=data['Likes'], video_id=data['video_id'], date=data['Date']) for data in comments if data['Comment'] not in exisiting_comments]

        if new_comments:
            session.bulk_save_objects(new_comments)
            session.commit()
            session.query(RawComments).all()
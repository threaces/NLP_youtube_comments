import re
import pandas as pd
from typing import Optional, Dict
from src.get_data import get_content
from support_elements import title_patterns

def parse_title(title: str, title_patterns: list) -> Optional[Dict]:
    
    """
    Parse video title to extract match information.
    Returns None if title doesn't match expected format.
    """
    
    for pattern in title_patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) == 4:
                if 'vs' in title and '(' in title:  # Handle "vs (score)" format
                    return {
                        'home_team': groups[0].strip().capitalize(),
                        'guest_team': groups[1].strip().capitalize(),
                        'home_score': int(groups[2]),
                        'guest_score': int(groups[3])
                    }
                else:  # Handle standard format
                    return {
                        'home_team': groups[0].strip().capitalize(),
                        'guest_team': groups[3].strip().capitalize(),
                        'home_score': int(groups[1]),
                        'guest_score': int(groups[2])
                    }
    return None

def parse_views(data_text: str) -> float:

    """
    Function to extract and convert text to number
    Args:
        data_text (str); Data dictionary from APi
    Returns:
        number (floar); Number of views for youtube video
    """
    
    number = data_text.replace('K views', '').replace('M views', '').strip()
    number = float(number)

    if 'K' in data_text:
        return number * 1000
    elif 'M' in data_text:
        return number * 1000000
    else:
        return number
    
def transform_data_input(req) -> list[dict]:

    """
    Function to extract information about youtube video like lenght.
    Function is also gathering data from other functions and saving them into list of dicts.

    Args:
        req; It's raw data collected from api
    Returns:
        video_details (list[dict]); List with information about youtube videos
    """

    video_items: list[dict] = []

    for movie_data in list(req):

        try:
            if int(movie_data['lengthSeconds']) > 210:
                continue

            video_id = str(movie_data['videoId'])
            video_length = int(movie_data['lengthSeconds'])
            views = parse_views(movie_data['videoInfo']['runs'][0]['text'])     
            title = movie_data['title']['runs'][0]['text']

            game_info = parse_title(title, title_patterns)

            if not game_info:
                continue

            video_info = {
                    'video_id': video_id,
                    'length [s]': video_length,
                    'views': views,
                    'home_team': game_info['home_team'],
                    'home_goals': game_info['home_score'],
                    'guest_team': game_info['guest_team'],
                    'guest_goals': game_info['guest_score'],
                    'result': 'win' if game_info['home_score'] > game_info['guest_score'] 
                         else 'draw' if game_info['home_score'] == game_info['guest_score'] 
                         else 'loss'
            }

            video_items.append(video_info)

        except (KeyError, IndexError, ValueError) as e:
            print(f"Error processing video: {e}")
            continue

    return video_items

def get_comments(yt_comments:dict, video_id:str) -> list[dict]: 
    
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

    comments_container = []

    for comment in yt_comments['items']:

        if comment['snippet']['totalReplyCount'] > 0:
            for reply in comment['replies']['comments']:

                dict_with_data = {}

                reply = reply['snippet']
                
                comment = str(reply['textDisplay'])
                likes_count = int(reply['likeCount'])
                publishe_date = reply['publishedAt']

                dict_with_data['Comment'] = comment
                dict_with_data['Likes'] = likes_count
                dict_with_data['Date'] = publishe_date
                dict_with_data['video_id'] = video_id

                comments_container.append(dict_with_data)
        else:
            dict_with_data = {}
            raw_data = comment['snippet']['topLevelComment']['snippet']

            comment = str(raw_data['textDisplay'])
            likes_count = int(raw_data['likeCount'])
            publishe_date = raw_data['publishedAt']

            dict_with_data['Comment'] = comment
            dict_with_data['Likes'] = likes_count
            dict_with_data['Date'] = publishe_date
            dict_with_data['video_id'] = video_id

            comments_container.append(dict_with_data)

    return comments_container

def prepare_comments_saving(yt_client, df:pd.DataFrame):

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

    raw_data_api = []
    comments_desc = []
    comments_desc_with_id = []

    table_columns = list(df.columns)

    for movie_id in df[table_columns[0]]:

        raw_data = get_content(yt_client, movie_id)
        raw_data_api.append(raw_data)

    for item in raw_data_api:
        match_comments = get_comments(item, movie_id)
        comments_desc.append(match_comments)

    counter = 0

    for comment in comments_desc:
        for match_data in comment:
            counter += 1
            match_data['Id'] = counter
            comments_desc_with_id.append(match_data)

    return comments_desc_with_id
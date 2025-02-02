import re
from typing import Optional, Dict
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
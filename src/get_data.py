
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
from service import youtube_api, playlists, rankings

import logging

logger = logging.getLogger(__name__)

def generate_melon_day_chart_playlist():
    chart_name = 'Melon'
    chart_type = 'DAY'

    latest_chart = rankings.get_latest_ranking(chart_name, chart_type)

    playlist_name = f'Melon DAY Chart - {latest_chart['date']}'
    playlist_description = f'Melon DAY Chart - {latest_chart['date']}'

    playlist = playlists.get_playlist_by_name(playlist_name)

    if playlist is not None and len(playlist['playlist_item']) == 100:
        return None

    response = youtube_api.create_playlist(playlist_name, playlist_description)
    logger.debug(response)

    if 'id' in response:
        playlist_id = response['id']
        playlist_item = []
        for index, rank in enumerate(latest_chart['ranking']):
            response = youtube_api.add_to_playlist(playlist_id, rank['youtube_video_id'], index)
            logger.debug(response)

            if 'snippet' in response:
                playlist_item.append({'title': response['snippet']['title'],
                                      'position': response['snippet']['position'],
                                      'youtube_video_id': response['snippet']['resourceId']['videoId']})

        playlist = {
            'chart': latest_chart['chart'],
            'type': latest_chart['type'],
            'date': latest_chart['date'],
            'playlist_name': playlist_name,
            'playlist_description': playlist_description,
            'playlist_id': playlist_id,
            'playlist_item': playlist_item}

        playlists.insert_playlist(playlist)

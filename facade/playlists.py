from service import playlists as playlists_service


def get_playlist(chart_name: str, chart_type: str, args: dict) -> dict:

    playlist_data = playlists_service.get_playlist_by_chart_and_type(chart_name, chart_type)
    playlist_data.pop('_id', None)

    return playlist_data

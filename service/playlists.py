from extensions import mongo


def get_playlist_by_chart_and_type(chart_name: str, chart_type: str):
    return mongo.db.playlists.find_one({'chart': chart_name, 'type': chart_type})


def get_playlist_by_name(playlist_name: str):
    return mongo.db.playlists.find_one({'playlist_name': playlist_name})


def insert_playlist(playlist: dict):
    return mongo.db.playlists.insert_one(playlist)

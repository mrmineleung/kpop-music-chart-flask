import logging

import flask
import google.oauth2.credentials
import googleapiclient.discovery

logger = logging.getLogger()

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

client_secrets_file = 'client_secret.json'


def create_playlist(playlist_name: str, playlist_description: str):
    if 'credentials' not in flask.session:
        logger.error('No credentials')
        # return flask.redirect(flask.url_for('google_oauth2.authorize'))

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": playlist_description
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )

    response = request.execute()
    return response


def add_to_playlist(playlistId: str, videoId: str, position: int):
    if 'credentials' not in flask.session:
        logger.error('No credentials')
        # return flask.redirect(flask.url_for('google_oauth2.authorize'))

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlistId,
                "position": position,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": videoId
                }
            }
        }
    )

    response = request.execute()
    return response

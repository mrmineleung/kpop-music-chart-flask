import datetime

from flask import Blueprint, jsonify, request, url_for, session, redirect
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from extensions import mongo

google_oauth2 = Blueprint('google_oauth2', __name__, url_prefix='/oauth/google')

CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


@google_oauth2.route('/authorize')
def authorize():
    # if session['credentials'] is not None:
    #     return {'token': session['credentials']['token'],
    #             'refresh_token': session['credentials']['refresh_token']}

    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for('google_oauth2.oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


@google_oauth2.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('google_oauth2.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    mongo.db.oauth2_credentials.insert_one(credentials_to_dict(credentials))

    return {'status': 'ok'}


@google_oauth2.route('/token')
def get_token():
    if 'credentials' not in session:
        session['credentials'] = mongo.db.oauth2_credentials.find_one({}, sort=[('datetime', -1)])

    if session['credentials'] is not None:
        return {'token': session['credentials']['token'],
                'refresh_token': session['credentials']['refresh_token']}


def credentials_to_dict(credentials):
    return {'datetime': datetime.datetime.now(),
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

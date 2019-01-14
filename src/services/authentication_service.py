from googleapiclient.discovery import build
from google.oauth2 import credentials
from google_auth_oauthlib import flow
from oauth2client import file, tools

from flask import url_for, session, redirect
from . import application
import os

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def credentials_to_dict(creds):
    return {'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes}


def create_auth_request():
    """
    This method requests a token from Google (redirecting the user to login and consent to their calendar data being
    used) and if so, Google will return an authorisation URL containing an authorisation code.
    :return: a redirect to our `/authenticate` url to handle the authorisation code
    """
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    _flow = flow.Flow.from_client_secrets_file(
        os.environ.get('OAUTH_CREDENTIALS'),
        scopes=SCOPES)

    _flow.redirect_uri = os.environ.get('REDIRECT_URI')
    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = _flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        approval_prompt="force",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    return redirect(authorization_url)


def authorize_user(request):
    """
    Extracts the authorisation code taken from the redirect and exchanges it for a token which we can then use on any
    method calling the Google Calendar API
    :param request: the request object supplied to the `authenticate` method
    :return:
    """
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state'] if 'state' in session else None

    _flow = flow.Flow.from_client_secrets_file(
        os.environ.get('OAUTH_CREDENTIALS'), scopes=SCOPES, state=state)
    _flow.redirect_uri = url_for('authentication_handler', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    _flow.fetch_token(authorization_response=authorization_response)
    application.logger.info('authorisation token acquired')

    # Store credentials in the session.
    creds = _flow.credentials

    return credentials_to_dict(creds)


def get_credentials():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = create_auth_request()
        creds = tools.run_flow(flow, store)
    return creds


def get_service():
    creds = credentials.Credentials(**session['credentials'])
    service = build('calendar', 'v3', credentials=creds)
    # refresh session credentials in case the access token has been updated
    session['credentials'] = credentials_to_dict(creds)
    return service

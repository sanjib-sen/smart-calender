from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def dayDiff(days):

    print(datetime.datetime.utcnow().isoformat()[:9] + str(
        int(datetime.datetime.utcnow().isoformat()[9:10]) + days) + datetime.datetime.utcnow().isoformat()[10:])
    return (datetime.datetime.utcnow().isoformat()[:9] + str(
        int(datetime.datetime.utcnow().isoformat()[9:10]) + days) + datetime.datetime.utcnow().isoformat()[10:])

def gcal(onlyTime, days):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('api/creds/token.json'):
        creds = Credentials.from_authorized_user_file('api/creds/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'api/creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('api/creds/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=dayDiff(2) + 'Z',
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        lst = []
        for event in events:
            if onlyTime == False:    start = event['start'].get('dateTime', event['start'].get('date'))
            else: start = event['start'].get('dateTime', event['start'].get('date'))[11:16]
            # print(event)
            templs = [start, event['summary']]
            lst.append(templs)
            # print(start, event['summary'])

            print(templs)

    except HttpError as error:
        print('An error occurred: %s' % error)
    return lst

if __name__ == '__main__':
    gcal(True, 1)
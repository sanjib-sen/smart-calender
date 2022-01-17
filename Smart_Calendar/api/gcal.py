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
    return (datetime.datetime.utcnow().isoformat()[:9] + str(
        int(datetime.datetime.utcnow().isoformat()[8:9]) + int(days)) + datetime.datetime.utcnow().isoformat()[10:])

def gcal(onlyTime, days=1, date=None):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    lst = []
    creds = None
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    if date == None:
        date = now
        dayInterval = dayDiff(days) + 'Z'
    else:
        date += 'Z'
        dayInterval = dayDiff(days) + 'Z'
    print(date)
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
        # Call the Calendar API  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        print(dayInterval)
        events_result = service.events().list(calendarId='primary', timeMin=date, timeMax=dayInterval,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
            return [["No","Event"]]

        # Prints the start and name of the next 10 events

        for event in events:
            if onlyTime == False:
                start = event['start'].get('dateTime', event['start'].get('date'))
            else:
                start = event['start'].get('dateTime', event['start'].get('date'))[11:16]
            # print(event)

            try:
                templs = [start, event['summary']]
            except:
                templs = [start, "Untitled"]

            lst.append(templs)
            # print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)
    return lst

def create(summary, date):
    event = {
        'summary': summary,
        'start': {
            'dateTime': date,
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    lst = []
    creds = None
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
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        print('An error occurred: %s' % error)
if __name__ == '__main__':
    create("bhh",datetime.datetime.utcnow().isoformat())

from __future__ import print_function
import datetime
import os.path
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import textwrap


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    # Modified to work on console, OP: https://learn.adafruit.com/raspberry-pi-e-ink-desk-calendar-using-python/event-calendar-code

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    dispenseEvents = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if 'PILL' in event['summary']:
            # dispenseEvents.append(event)

            # Check for duplicates
            if dispenseEvents:
                duplicate = false
                for item in dispenseEvents:
                    if item.cal_id == event['id']:
                        duplicate = true

                # if not duplicate:
                    # newItem = dispenseItem(cal_id, start_month, start_day, hour, minute)

            print("dateTime: " + event['start'].get('dateTime'))
            parts = event['start'].get('dateTime').split('T')
            dateParts = parts[0].split('-')
            dispenseTimeParts = parts[1].split(':')
            print(parts)
            print(dateParts)
            print("time: " + dispenseTimeParts[0] + ":" + dispenseTimeParts[1])
            # print("Date: " + event['start'].get('date'))
            print("Time Zone: " + event['start'].get('timeZone'))
            print("ID: " + event['id'])


if __name__ == '__main__':
    main()
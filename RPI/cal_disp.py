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
from bluepy import btle
import binascii


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    # Modified to work on console, OP: https://learn.adafruit.com/raspberry-pi-e-ink-desk-calendar-using-python/event-calendar-code

    print("Connecting...")
    dev = btle.Peripheral("7c:87:ce:13:5e:da") # board3

    print("Services...")
    for svc in dev.services:
        print(str(svc))

    bracelet = btle.UUID("4fafc201-1fb5-459e-8fcc-c5c9c331914b")
    service = dev.getServiceByUUID(bracelet)

    chtruuid = btle.UUID("beb5483e-36e1-4688-b7f5-ea07361b26a8")
    chtr = service.getCharacteristics(chtruuid)[0]

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

    while(1):
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
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
                dispenseEvents.append(event)
            print(start, event['summary'])

        if not dispenseEvents:
            print('No PILL events found.')

        else:
            print('---PILL DISPENSING EVENTS---')
            for event in dispenseEvents:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event['summary'])
                chtr.write(str.encode("dispensing"))
                time.sleep(2)
                chtr.write(str.encode("normal"))
        print('-------------------------------------')
        print('-----CHECKING AGAIN IN 3 SECONDS-----')
        print('-------------------------------------')
        time.sleep(3)


if __name__ == '__main__':
    main()
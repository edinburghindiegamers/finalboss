import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate() -> Credentials:
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_event(
        summary:str,
        description:str,
        start: datetime.datetime,
        end: datetime.datetime,
        id:str=None,
        colour=None,
        location:str=None,
        recurrence:list=None,
        attendees:list=None,
        reminders:list=None
    ):
    creds = authenticate()
    try:
        service = build('calendar', 'v3', credentials=creds)
        event_body = {
            'id': id,
            'summary': summary,
            'location': location if location else 'On-Line Event (Discord)',
            'description': description,
            'colorId': str(colour) if colour else None,
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': str(start.tzinfo),
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': str(end.tzinfo),
            },
            'recurrence': recurrence,
            'attendees': attendees,
            'reminders': {
                'useDefault': True if not reminders else False,
                'overrides': reminders
            }
        }
        event = service.events().insert(calendarId='primary', body=event_body).execute()
        return event
    except Exception as error:
        raise error

def delete_event(id:str):
    creds = authenticate()
    try:
        service = build('calendar', 'v3', credentials=creds)
        service.events().delete(calendarId='primary', eventId=id).execute()
    except Exception as error:
        raise error

def update_event(id:str,
    summary:str,
    description:str,
    start: datetime.datetime,
    end: datetime.datetime,
    colour=None,
    location:str=None,
    recurrence:list=None,
    attendees:list=None,
    reminders:list=None
):
    creds = authenticate()
    try:
        service = build('calendar', 'v3', credentials=creds)
        event_body = service.events().get(calendarId='primary', eventId=id).execute()
        event_body['summary'] = summary
        event_body['location'] = location if location else 'On-Line Event (Discord)'
        event_body['description'] = description
        event_body['colorId'] = str(colour) if colour else None
        event_body['start'] = {
            'dateTime': start.isoformat(),
            'timeZone': str(start.tzinfo)
        }
        event_body['end'] = {
            'dateTime': end.isoformat(),
            'timeZone': str(end.tzinfo)
        }
        event_body['recurrence'] = recurrence
        event_body['attendees'] = attendees
        event_body['reminders'] = {
            'useDefault': True if not reminders else False,
            'overrides': reminders
        }
        event = service.events().update(calendarId='primary', eventId=id, body=event_body).execute()
        return event
    except Exception as error:
        raise error

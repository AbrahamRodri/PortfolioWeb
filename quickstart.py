import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Path to the service account key file
SERVICE_ACCOUNT_FILE = '/home/rodriguezabrahamdev/service_account.json'
# Scopes required for the calendar access
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# Authenticate and create a service object
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    try:
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId='rodriguez.abraham6369@gmail.com',
                timeMin=now,
                maxResults=10,  # Adjust the number of events as needed
                singleEvents=True,
                orderBy='startTime'
            )
            .execute()
        )
        events = events_result.get('items', [])

        if not events:
            print("No upcoming events found.")
            return []

        # Process and return the upcoming events
        event_list = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            event_list.append({
                'id': event.get("id"),
                'title': event.get("summary"),
                'start': start,
                'end': end,
                'description': event.get("description"),
                'recurrence' : event.get("recurrence")  # Corrected spelling
            })

        return event_list

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

# Get today's date
today = datetime.today()

# Calculate the date one week ago
one_week_ago = today - timedelta(weeks=1)

# Format the date in 'YYYY/MM/DD' format for use in Gmail API queries
one_week_ago_formatted = one_week_ago.strftime('%Y/%m/%d')

# If modifying these SCOPES, delete the token file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file with the token stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(os.getenv('TOKEN_FILE')):
        creds = Credentials.from_authorized_user_file(os.getenv('TOKEN_FILE'), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv('CREDENTIALS_FILE'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.getenv('TOKEN_FILE'), 'w') as token:
            token.write(creds.to_json())

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_unread_messages():
    service = authenticate_gmail()
    # Get unread messages
    results = service.users().messages().list(userId='me', q=f"is:unread category:primary after:{one_week_ago_formatted}").execute()
    messages = results.get('messages', [])

    unread_subjects = []

    if not messages:
        return 'No new unread messages found.'
    else:
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            sender = ''
            subject = ''
            for header in msg_data['payload']['headers']:
                if header['name'] == 'From':
                    sender += header['value']
                if header['name'] == 'Subject':
                    subject = header['value']
            unread_subjects.append(f'{sender}: {subject}')        
                    

    output = 'New emails:\n\n'
    for i, subject in enumerate(unread_subjects[:10], 1):
        output += f"{i}. {subject}\n"


    return output

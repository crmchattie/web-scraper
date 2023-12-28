from google.oauth2 import service_account
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = 'service_account_sw.json'
# The file downloaded from Google Cloud Console
CREDENTIALS_FILE = 'credentials_sw.json'
# The file where access tokens will be stored
TOKEN_FILE = 'token.pickle'

def authenticate_with_oauth():
    print("Starting authentication process...")
    creds = None

    # Check if the token file exists and load it
    if os.path.exists(TOKEN_FILE):
        print(f"Token file {TOKEN_FILE} found, loading...")
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
            print("Token loaded from file.")

    # Check if credentials are not available or valid
    if not creds or not creds.valid:
        print("No valid credentials, need to authenticate.")
        print("Initiating new authentication flow...")
        # flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        # creds = flow.run_local_server(port=0)
        print("Authentication flow completed.")
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
            print("Credentials refreshed.")
        else:
            print("Initiating new authentication flow...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            print("Authentication flow completed.")

        # Save the credentials for the next run
        print(f"Saving credentials to {TOKEN_FILE}...")
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
            print("Credentials saved.")

    else:
        print("Existing credentials are valid.")

    return creds

def get_credentials():
    print("Getting credentials...")
    creds = None
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        print("Service account file found. Loading...")
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    else:
        print("Service account file not found.")

    if not creds or not creds.valid:
        print("No valid credentials. Need to authenticate using the service account.")
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        print("Authentication using service account completed.")

        
    print("Valid:", creds.valid)
    print("Service Account Email:", getattr(creds, 'service_account_email', 'Not Available'))
    print("Scopes:", creds.scopes)
    print("Token:", getattr(creds, 'token', 'Not Available'))
    print("Refresh Token:", getattr(creds, 'refresh_token', 'Not Available'))
    print("Token URI:", getattr(creds, 'token_uri', 'Not Available'))
    print("Client ID:", getattr(creds, 'client_id', 'Not Available'))
    print("Client Secret:", getattr(creds, 'client_secret', 'Not Available'))
    print("Expiry:", getattr(creds, 'expiry', 'Not Available'))

    print("Credentials are valid.")
    return creds

def test_google_sheets_api():
    creds = authenticate_with_oauth()
    service = build('sheets', 'v4', credentials=creds)
    # Test read from a sheet (replace with your sheet ID and range)
    sheet_id = 'your_sheet_id_here'
    range_name = 'Sheet1!A1'
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_name).execute()
    print(result)

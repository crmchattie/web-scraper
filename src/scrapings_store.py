from googleapiclient.discovery import build
from .google_api_utils import authenticate_with_oauth

def update_google_sheet(sheet_id, range_name, values):
    print("update_google_sheet")
    """Update given range in Google Sheet with provided values."""
    creds = authenticate_with_oauth()
    if not creds or not creds.valid:
        print("Invalid credentials")
        return None

    try:
        service = build('sheets', 'v4', credentials=creds)
        body = {'values': values}
        result = service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        return result
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")
        print("range_name", range_name)
        print("range_values", values)
        return None
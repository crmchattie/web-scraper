from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .google_api_utils import authenticate_with_oauth

def get_starting_row(range_name):
    """Extract the starting row number from the range name."""
    if '!' in range_name:
        range_part = range_name.split('!')[1]
        for i, char in enumerate(range_part):
            if char.isdigit():
                return int(range_part[i:].split(':')[0])
    return 1  # Default to 1 if no row number is found

def get_domains(sheet_id, range_name):
    """Retrieve list of domains and their row numbers from a specified range in a Google Sheet."""
    print("Starting get_domains function.")

    # Get credentials
    creds = authenticate_with_oauth()
    print("Credentials obtained.")

    if not creds.valid:
        print("creds are not valid")
        return []

    # Initialize the Sheets API service
    try:
        service = build('sheets', 'v4', credentials=creds)
        print("Sheets service built successfully.")
    except Exception as e:
        print("Error building Sheets service:", e)
        return []

    # Call the Sheets API
    try:
        sheet = service.spreadsheets()
        print("Sheet object obtained.")
        print("sheet_id", sheet_id)
        print("range_name", range_name)
        result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
        print("API call executed.")
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    except Exception as e:
        print(f"A general error occurred: {e}")
        return None

    # Process the results
    try:
        values = result.get('values', [])
        print("values: ", values)

        if not values:
            print('No data found.')
            return []

        starting_row = get_starting_row(range_name)

        # Pair each domain with its row number
        domains_with_rows = [(row[0], index + starting_row) for index, row in enumerate(values) if row]
        print("domains_with_rows: ", domains_with_rows)
        return domains_with_rows
    except Exception as e:
        print("Error processing API response:", e)
        return []

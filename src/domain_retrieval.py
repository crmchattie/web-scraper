from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .google_api_utils import authenticate_with_oauth
from src.helpers import is_content_empty

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
        # Modify the range_name if necessary to include the additional columns
        result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
        values = result.get('values', [])
        print("values: ", values)

        if not values:
            print('No data found.')
            return []

        starting_row = get_starting_row(range_name)
        domains_with_data = []

        for index, row in enumerate(values):
            print("get_domains", row)
            domain = row[0] if row else None
            print("get_domains", domain)

            # Check if additional data is present
            if len(row) > 11:
                # summary = row[5]
                data = {
                    "title": row[6],
                    "name": row[7],
                    "meta_description": row[8],
                    "headings": row[9],  # Convert to correct format if necessary
                    "navigation": row[10],
                    "main_content": row[11],
                    "links": row[12]  # Convert to correct format if necessary
                }
                print("get_domains", data)
                # Include domain if any of the data is non-empty and doesn't match 'is_content_empty'
                if not all(is_content_empty(data[key], key) for key in data):
                    domains_with_data.append((domain, index + starting_row, data))
            else:
                # No additional data, set data to None
                domains_with_data.append((domain, index + starting_row, None))

        print("domains_with_data: ", domains_with_data)
        return domains_with_data
    except Exception as e:
        print("Error processing API response:", e)
        return []

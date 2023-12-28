from googleapiclient.discovery import build
from .google_api_utils import authenticate_with_oauth

def create_and_store_dictionaries(sheet_id):
    # Authenticate and build the service
    creds = authenticate_with_oauth()
    print("Credentials obtained.")

    if not creds.valid:
        print("creds are not valid")
        return

    service = build('sheets', 'v4', credentials=creds)

    # IDs and ranges
    categories_range = 'Categories_Dupes!A:D'  # Adjust the range as needed

    # Get data from 'Categories_Dupes' sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=categories_range).execute()
    rows = result.get('values', [])

    # Initialize dictionaries
    sector_to_sector = []
    sector_to_subsector = {}
    subsector_to_industry = {}
    industry_to_subindustry = {}

    for row in rows[1:]:
        # Unpack values safely
        sector = row[0] if len(row) > 0 else None
        subsector = row[1] if len(row) > 1 else None
        industry = row[2] if len(row) > 2 else None
        subindustry = row[3] if len(row) > 3 else None

        if sector:
            sector_to_sector.append(sector)
            if subsector:
                sector_to_subsector.setdefault(sector, set()).add(subsector)
                if industry:
                    subsector_to_industry.setdefault(subsector, set()).add(industry)
                    if subindustry:
                        industry_to_subindustry.setdefault(industry, set()).add(subindustry)

    sector_to_sector = list(set(sector_to_sector))  # Remove duplicates
    sector_to_subsector = {k: list(v) for k, v in sector_to_subsector.items()}
    subsector_to_industry = {k: list(v) for k, v in subsector_to_industry.items()}
    industry_to_subindustry = {k: list(v) for k, v in industry_to_subindustry.items()}

    print("sector_to_sector =", sector_to_sector)
    print("sector_to_subsector =", sector_to_subsector)
    print("subsector_to_industry =", subsector_to_industry)
    print("industry_to_subindustry =", industry_to_subindustry)

    print("Dictionaries updated in 'Dictionaries' sheet.")
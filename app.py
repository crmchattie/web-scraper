from flask import Flask, jsonify
from bs4 import BeautifulSoup
from src.webdriver_setup import setup_headless_selenium_driver, setup_head_selenium_driver
from src.domain_retrieval import get_domains
from src.scrapings_grab import get_page_source, parse_for_site_name, parse_for_title, parse_for_meta_description, parse_for_headings, parse_for_navigation, parse_for_main_content, parse_for_links
from src.translate_text import translate_text
from src.analyze_text import analyze_website_content, categorize_website_sector, categorize_website_subsector, categorize_website_industry, categorize_website_subindustry, categorize_website_sector_w_new_categories, categorize_website_subsector_w_new_categories, categorize_website_industry_w_new_categories, categorize_website_subindustry_w_new_categories
from src.scrapings_store import update_google_sheet
# from src.quickstart import main

app = Flask(__name__)

SPREADSHEET_ID = '16oES5lHLxfjdcaBYeRfIy2RNFArIsH-dT2nSJibZ9PQ'
SPREADSHEET_NAME = 'Domains'
DOMAIN_RANGE = f'{SPREADSHEET_NAME}!A2:A100'

# Define a Flask route
@app.route('/run-script')
def run_script():
    try:
        driver = setup_headless_selenium_driver()
        if driver is None:
            print("Driver returned none")

        domains_with_rows = get_domains(SPREADSHEET_ID, DOMAIN_RANGE)

        for domain, row_number in domains_with_rows:
            print("domain: ", domain)
            print("row_number: ", row_number)
            page_source = get_page_source(domain, driver)
            if isinstance(page_source, str):
                soup = BeautifulSoup(page_source, 'html.parser')

                # Gather data from the soup
                title = parse_for_title(soup)
                name = parse_for_site_name(soup)
                meta_description = parse_for_meta_description(soup)
                headings = parse_for_headings(soup)
                navigation = parse_for_navigation(soup)
                main_content = parse_for_main_content(soup)
                links = parse_for_links(soup)

                data_to_write = []

                if (title == "No title found" and
                    name == "No site name found" and
                    meta_description == "No meta description found" and
                    navigation == "No navigation items found" and
                    main_content == "No main content found"):
                    data_to_write = [
                        "None",
                        "None",
                        "None",
                        "None",
                        "None",
                        str(title),
                        str(name),
                        str(meta_description),
                        str(headings),
                        str(navigation),
                        str(main_content),
                        str(links)
                    ]
                else:
                    # Translate scraped data
                    translated_title = translate_text(str(title), "auto", "en")  # Auto-detect language to Spanish
                    translated_name = translate_text(str(name), "auto", "en")  # Auto-detect language to Spanish
                    translated_meta_description = translate_text(str(meta_description), "auto", "en")
                    translated_headings = translate_text(str(headings), "auto", "en")  # Joining text for simplicity
                    translated_navigation = translate_text(str(navigation), "auto", "en")  # Joining text for simplicity
                    translated_main_content = translate_text(str(main_content), "auto", "en")  # Joining text for simplicity
                    translated_links = translate_text(str(links), "auto", "en")  # Joining text for simplicity

                    summary = analyze_website_content(domain, translated_title, translated_meta_description, translated_headings, translated_navigation, translated_main_content)
                    sector = categorize_website_sector_w_new_categories(summary)
                    subsector = categorize_website_subsector_w_new_categories(summary, sector)
                    industry = categorize_website_industry_w_new_categories(summary, subsector)
                    subindustry = categorize_website_subindustry_w_new_categories(summary, industry)

                    print("summary", summary)
                    print("sector", sector)
                    print("subsector", subsector)
                    print("industry", industry)
                    print("subindustry", subindustry)

                    # Prepare data to be written to the sheet
                    data_to_write = [
                        str(sector),
                        str(subsector),
                        str(industry),
                        str(subindustry),
                        str(summary),
                        translated_title,
                        translated_name,
                        translated_meta_description,
                        translated_headings,
                        translated_navigation,
                        translated_main_content,
                        translated_links
                    ]

                # Update the Google Sheet
                # Adjust the range_to_update as necessary to match the structure of your sheet
                start_column = 'B'  # Starting column
                end_column = chr(ord(start_column) + len(data_to_write) - 1)  # Calculate ending column
                range_to_update = f'{SPREADSHEET_NAME}!{start_column}{row_number}:{end_column}{row_number}'
                update_google_sheet(SPREADSHEET_ID, range_to_update, [data_to_write])

        driver.quit()
        return jsonify({'status': 'success', 'message': 'Script executed successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    with app.app_context():
        run_script()

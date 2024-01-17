from flask import Flask, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from bs4 import BeautifulSoup
from src.webdriver_setup import setup_headless_playwright_driver, setup_head_playwright_driver, setup_headless_selenium_driver, setup_head_selenium_driver
from src.domain_retrieval import get_domains
from src.scrapings_grab import get_page_source_selenium, get_page_source_playwright, parse_for_site_name, parse_for_title, parse_for_meta_description, parse_for_headings, parse_for_navigation, parse_for_main_content, parse_for_links, parse_for_body
from src.translate_text import translate_text
from src.analyze_text import analyze_website_content_summary, analyze_website_content_product, categorize_website_sector, categorize_website_subsector, categorize_website_industry, categorize_website_subindustry, categorize_website_sector_w_new_categories, categorize_website_subsector_w_new_categories, categorize_website_industry_w_new_categories, categorize_website_subindustry_w_new_categories
from src.scrapings_store import update_google_sheet
from src.helpers import is_content_empty, simplify_structure
import asyncio
# from src.quickstart import main

app = Flask(__name__)

SPREADSHEET_ID = '16oES5lHLxfjdcaBYeRfIy2RNFArIsH-dT2nSJibZ9PQ'
SPREADSHEET_NAME = 'Domains'
DOMAIN_RANGE = f'{SPREADSHEET_NAME}!A16544:M16733'
BATCH_SIZE = 25
MAX_WORKERS = 4

async def web_scraping(domain):
    print(f"Scraping: {domain}")
    try:
        # Add your scraping logic here
        page_source = await get_page_source_playwright(domain)
        return page_source
    except Exception as e:
        print(f"Error occurred while scraping {domain}: {e}")
        return None

def translate_data(data):
    # Assuming 'data' is a dictionary containing the elements to be translated
    translated_data = {key: translate_text(str(value), "auto", "en") for key, value in data.items()}
    return translated_data

def analyze_and_categorize(domain, translated_data):
    # Assuming 'translated_data' contains necessary elements like title, name, etc.
    summary = analyze_website_content_summary(domain, translated_data['title'], translated_data['meta_description'], translated_data['headings'], translated_data['navigation'], translated_data['main_content'], translated_data['links'])
    # product = analyze_website_content_product(domain, translated_data['title'], translated_data['meta_description'], translated_data['headings'], translated_data['navigation'], translated_data['main_content'], translated_data['links'])
    sector = categorize_website_sector_w_new_categories(summary)
    subsector = categorize_website_subsector_w_new_categories(summary, sector)
    industry = categorize_website_industry_w_new_categories(summary, subsector)
    subindustry = categorize_website_subindustry_w_new_categories(summary, industry)
    return sector, subsector, industry, subindustry, summary

def update_sheet_from_queue(results_queue):
    print("update_sheet_from_queue")
    results = []
    while not results_queue.empty() and len(results) < BATCH_SIZE:
        results.append(results_queue.get())

    # Sort the results by row number
    results.sort(key=lambda x: x[0])

    # Update the Google Sheet with the batch of results
    for row_number, data_to_write in results:
        print("update_sheet_from_queue domain", row_number)
        print("update_sheet_from_queue data_to_write", data_to_write)
        update_google_sheet(SPREADSHEET_ID, f'{SPREADSHEET_NAME}!B{row_number}', [data_to_write])

def process_domain(domain, row_number, data, results_queue):
    print("process_domain", domain)
    print("process_domain", data)
    try:
        # Web scraping (if page_source not provided)
        if not data:
            page_source = asyncio.run(web_scraping(domain))
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extract data
            data = {
                "title": parse_for_title(soup),
                "name": parse_for_site_name(soup),
                "meta_description": parse_for_meta_description(soup),
                "headings": parse_for_headings(soup),
                "navigation": parse_for_navigation(soup),
                "main_content": parse_for_main_content(soup),
                "links": parse_for_links(soup)
            }
            soup.decompose()
        if data:

            # Check if the data meets the 'empty' criteria
            if all(is_content_empty(value, key) for key, value in data.items()):
                simplified_data = {key: simplify_structure(value) for key, value in data.items()}
                data_to_write = ["None", "None", "None", "None", "None", *simplified_data.values()]
            else:
                # Proceed with translation and further processing
                # translated_data = translate_data(data)
                translated_data = data
                simplified_data = {key: simplify_structure(value) for key, value in translated_data.items()}
                sector, subsector, industry, subindustry, summary = analyze_and_categorize(domain, simplified_data)
                data_to_write = [sector, subsector, industry, subindustry, summary, *simplified_data.values()]
            results_queue.put((row_number, data_to_write))
        else:
            print(f"No content available for domain {domain}")

    except Exception as e:
        print(f"An error occurred while processing {domain}: {e}")
    
@app.route('/run-script')
def run_script():
    try:
        domains_with_rows = get_domains(SPREADSHEET_ID, DOMAIN_RANGE)
        results_queue = Queue()

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Create a list of futures
            futures = []
            # Dictionary to map futures to domain and row number
            future_to_domain = {}

            for domain, row_number, data in domains_with_rows:
                print(f"Scheduling domain processing for: {domain}")
                future = executor.submit(process_domain, domain, row_number, data, results_queue)
                futures.append(future)
                # Map the future to its domain and row number
                future_to_domain[future] = (domain, row_number)

            for future in as_completed(futures):
                domain, row_number = future_to_domain[future]
                try:
                    # Wait for the future to complete and get its result
                    future.result()
                    print(f"Successfully processed domain {domain} at row {row_number}")

                    print(f"results_queue.qsize() {results_queue.qsize()}")
                    # Check if the results queue has reached the batch size
                    if results_queue.qsize() >= BATCH_SIZE:
                        update_sheet_from_queue(results_queue)

                except Exception as e:
                    # Log any exceptions encountered
                    print(f"Error processing domain {domain} at row {row_number}: {e}")

        # Update the sheet with any remaining results
        update_sheet_from_queue(results_queue)

        return jsonify({'status': 'success', 'message': 'Script executed successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    with app.app_context():
        run_script()

from flask import Flask, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from bs4 import BeautifulSoup
from src.webdriver_setup import setup_headless_playwright_driver, setup_head_playwright_driver, setup_headless_selenium_driver, setup_head_selenium_driver
from src.domain_retrieval import get_domains
from src.scrapings_grab import get_page_source_selenium, get_page_source_playwright, parse_for_site_name, parse_for_title, parse_for_meta_description, parse_for_headings, parse_for_navigation, parse_for_main_content, parse_for_links, parse_for_body
from src.translate_text import translate_text
from src.analyze_text import analyze_website_content, categorize_website_sector, categorize_website_subsector, categorize_website_industry, categorize_website_subindustry, categorize_website_sector_w_new_categories, categorize_website_subsector_w_new_categories, categorize_website_industry_w_new_categories, categorize_website_subindustry_w_new_categories
from src.scrapings_store import update_google_sheet
import asyncio
import tracemalloc
from tracemalloc import Snapshot
# from src.quickstart import main

app = Flask(__name__)

SPREADSHEET_ID = '16oES5lHLxfjdcaBYeRfIy2RNFArIsH-dT2nSJibZ9PQ'
SPREADSHEET_NAME = 'Domains'
DOMAIN_RANGE = f'{SPREADSHEET_NAME}!A5001:A7000'
BATCH_SIZE = 25
MAX_WORKERS = 4

def display_top(statistics, limit=10):
    print("Top {} lines".format(limit))
    for index, stat in enumerate(statistics[:limit], 1):
        frame = stat.traceback[0]
        filename = getattr(frame, 'filename', 'unknown')
        lineno = getattr(frame, 'lineno', 'unknown')
        print(f"#{index}: {filename}:{lineno}: {stat.size / 1024:.1f} KiB")
        for line in stat.traceback.format():
            print(line)

    other = statistics[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print(f"{len(other)} other: {size / 1024:.1f} KiB")
    total = sum(stat.size for stat in statistics)
    print(f"Total allocated size: {total / 1024:.1f} KiB")

def process_domain(domain, row_number, results_queue):
    try:
        driver = setup_headless_selenium_driver()
        if driver is None:
            print("Driver returned none")

        page_source = get_page_source_selenium(domain, driver)
        # page_source = asyncio.run(get_page_source_playwright(domain))
        # print("process_domain", domain)
        # print("process_domain", page_source)

        if page_source and isinstance(page_source, str):
            soup = BeautifulSoup(page_source, 'html.parser')
            
            title = parse_for_title(soup)
            name = parse_for_site_name(soup)
            meta_description = parse_for_meta_description(soup)
            headings = parse_for_headings(soup)
            navigation = parse_for_navigation(soup)
            main_content = parse_for_main_content(soup)
            links = parse_for_links(soup)

            # Add your logic to process and extract the necessary data
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
                    str(links),
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
                    translated_links,
                ]

            soup.decompose()
            results_queue.put((row_number, data_to_write))
        
        else:
            print(f"No HTML content retrieved for domain {domain}, {page_source[:500]}")
        
        driver.quit()
        
    except Exception as e:
        print(f"An error occurred while processing {domain}: {e}")

def update_sheet_from_queue(results_queue):
    print("update_sheet_from_queue")
    results = []
    while not results_queue.empty() and len(results) < BATCH_SIZE:
        results.append(results_queue.get())

    # Sort the results by row number
    results.sort(key=lambda x: x[0])

    # Update the Google Sheet with the batch of results
    for row_number, data_to_write in results:
        update_google_sheet(SPREADSHEET_ID, f'{SPREADSHEET_NAME}!B{row_number}', [data_to_write])
    
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

            for domain, row_number in domains_with_rows:
                future = executor.submit(process_domain, domain, row_number, results_queue)
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

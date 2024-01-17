import time
import asyncio
from playwright.async_api import async_playwright
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
from playwright.async_api import async_playwright
import random

async def custom_logger(name: str, severity: str, message: str, args: str):
    if name == 'browser':
        print(f"{name} {message}")

async def get_page_source_playwright(domain):
    print("get_page_source")
    https_domain = 'https://' + domain if not domain.startswith('http://') and not domain.startswith('https://') else domain
    http_domain = 'http://' + domain if not domain.startswith('http://') and not domain.startswith('https://') else domain
    
    # Define a list of user agent strings
    user_agent_strings = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    ]

    try:
        async with async_playwright() as p:
            # Launch the browser in non-headless mode for debugging
            browser = await p.chromium.launch()

            # Create a new context with a random user agent
            context = await browser.new_context(
                user_agent=random.choice(user_agent_strings)
            )

            # Add JavaScript to be executed before any other script on each page
            await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            page = await context.new_page()

            # Listen to various events
            # page.on('request', lambda request: print(f'Request made: {request.url}'))
            # page.on('response', lambda response: print(f'Response received: {response.url} - {response.status}'))
            # page.on('console', lambda msg: print(f'Console message: {msg.text}'))
            # page.on('load', lambda: print('Page loaded'))
            # page.on('domcontentloaded', lambda: print('DOM content loaded'))
            # page.on('requestfailed', lambda request: print(f'Request failed: {request.url}'))

            try:
                # First, try with https
                await page.goto(https_domain, wait_until="load", timeout=15000)
            except Exception as e:
                print(f"Failed to load https version: {e}, trying http version")
                # If https fails, try with http
                await page.goto(http_domain, wait_until="load", timeout=15000)
            
            page_source = await page.content()
            await browser.close()
            return page_source
    except Exception as e:
        print(f"Error occurred while fetching page source: {domain} {e}")
        return None

    
def get_page_source_selenium(domain, driver):
    print("get_page_source")
    """Fetch the page source for a given domain using Selenium."""
    formatted_domain = 'https://' + domain if not domain.startswith('http://') and not domain.startswith('https://') else domain
    try:
        driver.get(formatted_domain)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return driver.page_source
    except Exception as e:
        return f"Error occurred while fetching page source: {e}"
    
def parse_for_body(soup):
    print("parse_for_body")
    """Parse the page source (soup) to extract the body content."""
    body = soup.find('body')
    if body:
        return str(body)  # Convert the body tag to string
    return 'No body content found'
    
def parse_for_site_name(soup):
    print("parse_for_site_name")
    """Parse the page source (soup) to extract the site name."""
    og_site_name = soup.find("meta", property="og:site_name")
    if og_site_name and og_site_name.get("content"):
        return og_site_name.get("content")

    twitter_site_name = soup.find("meta", property="twitter:title")
    if twitter_site_name and twitter_site_name.get("content"):
        return twitter_site_name.get("content")

    return 'No site name found'
    
def parse_for_title(soup):
    print("parse_for_title")
    """Parse the page source (soup) to extract the title."""
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    elif soup.find("meta", property="og:title"):
        return soup.find("meta", property="og:title").get('content')
    elif soup.find("meta", property="twitter:title"):
        return soup.find("meta", property="twitter:title").get('content')
    return 'No title found'

def parse_for_meta_description(soup):
    print("parse_for_meta_description")
    """Parse the page source (soup) to extract the meta description."""
    meta_tag = soup.find("meta", attrs={"name": "description"}) or \
               soup.find("meta", property="og:description") or \
               soup.find("meta", property="twitter:description")
    if meta_tag:
        return meta_tag.get('content')
    return 'No meta description found'
    
def parse_for_headings(soup):
    print("parse_for_headings")
    """Parse the page source (soup) to extract headings."""
    headings = {}
    for i in range(1, 7):
        headings[f'h{i}'] = [h.text.strip() for h in soup.find_all(f'h{i}')]
    return headings

def parse_for_navigation(soup):
    print("parse_for_navigation")
    """Parse the page source (soup) to extract navigation menu items."""
    nav_items = []
    nav = soup.find('nav')
    if nav:
        links = nav.find_all('a')
        nav_items = [link.text.strip() for link in links]
    return nav_items if nav_items else 'No navigation items found'

def parse_for_main_content(soup):
    print("parse_for_main_content")
    """Parse the page source (soup) to extract the main body content."""
    paragraphs = [p.text.strip() for p in soup.find_all('p')]
    return paragraphs if paragraphs else 'No main content found'

def parse_for_images(soup):
    print("parse_for_images")
    """Parse the page source (soup) to extract images and their alt text."""
    images = [{'src': img['src'], 'alt': img.get('alt', 'No alt text')} for img in soup.find_all('img')]
    return images if images else 'No images found'

def parse_for_links(soup):
    print("parse_for_links")
    """Parse the page source (soup) to extract internal links."""
    # links = {'internal': [], 'external': []}
    links = {'internal': []}
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('/'):
            links['internal'].append(href)
        # else:
        #     links['external'].append(href)
    return links

def parse_for_footer(soup):
    print("parse_for_footer")
    """Parse the page source (soup) to extract footer information."""
    footer = soup.find('footer')
    return footer.text.strip() if footer else 'No footer information found'

def parse_for_social_media_links(soup):
    print("parse_for_social_media_links")
    """Parse the page source (soup) to extract social media links."""
    social_media_links = []
    # Common patterns for social media links
    patterns = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com']
    for link in soup.find_all('a', href=True):
        if any(social in link['href'] for social in patterns):
            social_media_links.append(link['href'])
    return social_media_links if social_media_links else 'No social media links found'




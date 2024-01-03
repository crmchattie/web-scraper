from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def setup_headless_selenium_driver():
    try:
        options = Options()
        options.add_argument("--headless")

        # Initialize the WebDriver with the options
        driver = webdriver.Firefox(options=options)

        # Below doesn't work; keeping it there in case we want to edit
        # # Create a new Firefox Profile
        # profile = FirefoxProfile()

        # # Set preferences (example: setting a custom user-agent)
        # profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)")

        # # Use the profile with Selenium
        # options = Options()
        # options.headless = True  # for headless mode
        # driver = webdriver.Firefox(firefox_profile=profile, options=options)

        # Set a specific window size
        driver.set_window_size(1920, 1080)

        return driver
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def setup_head_selenium_driver():
    try:
        # Set up your Selenium WebDriver here
        driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH or specify path directly
        return driver
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
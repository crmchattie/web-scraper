from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def setup_headless_selenium_driver():
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    return driver

def setup_head_selenium_driver():
    # Set up your Selenium WebDriver here
    driver = webdriver.Chrome()  # Ensure ChromeDriver is in your PATH or specify path directly
    return driver
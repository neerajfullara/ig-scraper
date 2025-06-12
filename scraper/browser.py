from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def init_browser(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    return driver

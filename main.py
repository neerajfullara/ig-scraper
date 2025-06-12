from scraper.browser import init_browser
from scraper.login import login
from scraper.scraper import scrape_reels
from config import USERNAME, PASSWORD

def main():
    driver = init_browser(headless=False)
    try:
        login(driver, USERNAME, PASSWORD)
        scrape_reels(driver, "example_username", max_count=5)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

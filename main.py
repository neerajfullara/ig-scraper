from scraper.browser import init_browser
from scraper.login import login
from scraper.scraper import scrape_reels
from config import USERNAME, PASSWORD
import time, random

ACCOUNT_LIST = [
    "accounts"
]

def main():
    driver = init_browser(headless=False)
    try:
        login(driver, USERNAME, PASSWORD)

        for account in ACCOUNT_LIST:
            print(f"\nStarting: @{account}")
            scrape_reels(driver, account, max_count=5)

            wait_time = random.uniform(30, 60)
            print(f"Cooling down {int(wait_time)}s...")
            time.sleep(wait_time)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

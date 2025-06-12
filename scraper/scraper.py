import time
import pandas as pd
from selenium.webdriver.common.by import By
from .utils import human_scroll

def scrape_reels(driver, account_name, max_count=10):
    print(f"Scraping Reels for @{account_name}...")
    driver.get(f"https://www.instagram.com/{account_name}/reels/")
    time.sleep(5)

    reels_links = set()
    while len(reels_links) < max_count:
        human_scroll(driver)
        reels = driver.find_elements(By.XPATH, '//a[contains(@href, "/reel/")]')
        for r in reels:
            href = r.get_attribute("href")
            if href and href not in reels_links:
                reels_links.add(href)
            if len(reels_links) >= max_count:
                break

    data = []
    for link in list(reels_links):
        driver.get(link)
        time.sleep(4)
        try:
            video_url = driver.find_element(By.TAG_NAME, "video").get_attribute("src")
        except:
            video_url = "N/A"
        try:
            caption = driver.find_element(By.XPATH, "//meta[@property='og:description']").get_attribute("content")
        except:
            caption = "N/A"

        data.append({
            "reel_url": link,
            "video_url": video_url,
            "caption": caption
        })

    df = pd.DataFrame(data)
    df.to_csv("data/reels_data.csv", index=False)
    print("Saved to data/reels_data.csv")

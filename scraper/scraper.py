import time
import os
import pandas as pd
import random
from selenium.webdriver.common.by import By
from .utils import human_scroll, retry

DEDUP_FILE = "scraped_reels.txt"

def load_scraped_reels():
    if os.path.exists(DEDUP_FILE):
        with open(DEDUP_FILE, "r") as f:
            return set(line.strip() for line in f)
    return set()

def save_scraped_reel(url):
    with open(DEDUP_FILE, "a") as f:
        f.write(url + "\n")

@retry(max_retries=3)
def scrape_single_reel(driver, link, influencer_name):
    driver.get(link)
    time.sleep(random.uniform(3, 5))

    data = {
        "reel_url": link,
        "influencer": influencer_name,
        "caption": "N/A",
        "views": "N/A",
        "likes": "N/A",
        "comments": "N/A",
    }

    try:
        # Actual caption: first span inside article
        # Sometimes it's deeply nested, this is common for reels
        spans = driver.find_elements(By.CLASS_NAME, "x193iq5w")
        for span in spans:
            txt = span.text.strip()
            if txt and len(txt) > 0:
                data["caption"] = txt
                break
    except: pass

    try:
        # Views: find span with "views"
        spans = driver.find_elements(By.XPATH, '//span[contains(text(),"views")]')
        for span in spans:
            text = span.text.strip().lower()
            if "views" in text:
                data["views"] = text.split()[0].replace(",", "")
                break
    except: pass

    try:
        # Likes: sometimes shown under views
        likes_spans = driver.find_elements(By.XPATH, '//section//span')
        for s in likes_spans:
            if "likes" in s.text.lower():
                data["likes"] = s.text.lower().split(" ")[0].replace(",", "")
                break
    except: pass

    try:
        # Comment count: count visible comment blocks
        comments = driver.find_elements(By.XPATH, '//ul/ul/div/li/div/div/div[2]/div/span')
        data["comments"] = str(len(comments))
    except: pass

    return data

def scrape_reels(driver, account_name, max_count=5):
    print(f"📸 Scraping Reels from @{account_name}")
    driver.get(f"https://www.instagram.com/{account_name}/reels/")
    time.sleep(5)

    reels_links = set()
    already_scraped = load_scraped_reels()

    while len(reels_links) < max_count:
        human_scroll(driver)
        reels = driver.find_elements(By.XPATH, '//a[contains(@href, "/reel/")]')
        for r in reels:
            href = r.get_attribute("href")
            if href and href not in reels_links and href not in already_scraped:
                reels_links.add(href)
            if len(reels_links) >= max_count:
                break

    data = []
    for link in list(reels_links):
        print(f"🔍 Scraping: {link}")
        result = scrape_single_reel(driver, link, account_name)
        data.append(result)
        save_scraped_reel(link)
        time.sleep(random.uniform(3, 6))  # Delay between reels

    # Ensure directory exists
    os.makedirs("data", exist_ok=True)

    df = pd.DataFrame(data)
    df.to_csv("data/reels_data.csv", mode='a', header=not os.path.exists("data/reels_data.csv"), index=False)

    print(f"✅ Saved {len(data)} reels to data/reels_data.csv")

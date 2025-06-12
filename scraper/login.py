import os
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

COOKIE_FILE = "session_cookies.pkl"

def login(driver, username, password):
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    # Try loading existing cookies.......
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://www.instagram.com/")
        time.sleep(3)

        # Check if still logged in....
        if "login" not in driver.current_url:
            print("Logged in with session cookies.")
            return

    print("Logging in manually...")
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")

    user_input.send_keys(username)
    pass_input.send_keys(password + Keys.RETURN)
    time.sleep(6)

    # Save new cookies......
    cookies = driver.get_cookies()
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(cookies, f)
    print("New session saved.")

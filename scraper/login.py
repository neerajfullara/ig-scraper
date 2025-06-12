import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def login(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)

    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")

    user_input.send_keys(username)
    pass_input.send_keys(password + Keys.RETURN)

    time.sleep(5)

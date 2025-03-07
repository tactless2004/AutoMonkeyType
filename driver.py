from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

if __name__ == "__main__":
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)  # Optional argument, if not specified will search path.

    driver.get("https://monkeytype.com/")

    sleep(1)

    # Accept Cookies
    button = driver.find_element(By.CLASS_NAME, "acceptAll")
    if button:
        button.click()

    # give the site a moment to refresh
    sleep(0.5)
    word = driver.find_element(By.CLASS_NAME, "word").text

    action = ActionChains(driver)
    action.send_keys(word)
    action.perform()

    # Let me see the results
    sleep(3)

    driver.close()
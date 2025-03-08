from time import sleep, time_ns
import argparse
from word_buffer import buf
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains # Sends generic (non-element specific) actions

def get_words(driver: webdriver) -> iter:
    words = driver.find_elements(By.CSS_SELECTOR, "div.word")
    return iter([word.text for word in words if word.get_attribute("class") != "word typed"])

            

if __name__ == "__main__":
    # selenium setup
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://monkeytype.com/")

    # Let the page load
    sleep(0.5)

    # Try Accept Cookies
    button = driver.find_element(By.CLASS_NAME, "acceptAll")
    if button:
        button.click()

    # give the site a moment to refresh
    sleep(0.5)


    initial_time = time_ns()
    running = True
    word_iterator = get_words(driver)
    action = ActionChains(driver)    
    stop_time = 31

    while running:
        try:
            word = next(word_iterator)
            action.send_keys(word)
            action.send_keys(" ")
            action.perform()
        except StopIteration:
            word_iterator = get_words(driver)
            continue
        except Exception as e:
            # Generic Exception, usually the typing page is dead 
            print(f"{e}")
            running = False

        # Check if its been > 30 seconds.
        if (time_ns() - initial_time)*1e-9 > stop_time:
            running = False


    sleep(30)
    driver.close()

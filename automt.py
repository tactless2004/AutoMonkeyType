from time import sleep, time_ns
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains # Sends generic (non-element specific) actions
import argparse

def get_words(driver: webdriver) -> iter:
    return iter([word.text for word in driver.find_elements(By.CSS_SELECTOR, "div.word") if word.get_attribute("class") != "word typed"])

if __name__ == "__main__":
    # selenium setup
    driver = webdriver.Chrome(service=Service(executable_path="chromedriver.exe"))
    driver.get("https://monkeytype.com/")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--wpm", help="Words Per Minute")
    args = parser.parse_args()
    wpm = args.wpm if args.wpm else 0
    try:
        delay = (60/int(wpm)) if args.wpm != "inf" and int(args.wpm) > 0 else 0
    except ValueError:
        delay = 0

    # Try Accept Cookies
    button = driver.find_element(By.CLASS_NAME, "acceptAll")
    if button:
        button.click()

    # give the site a moment to refresh
    sleep(0.5)

    
    word_iterator = get_words(driver)
    action = ActionChains(driver)    

    start_time = time_ns()
    running = True
    while running:
        try:
            action.send_keys(f"{next(word_iterator)} ")
            action.perform()
        except StopIteration:
            word_iterator = get_words(driver)
            continue
        except Exception as e:
            # Generic Exception, usually the typing page is dead 
            print(f"{e}")
            running = False
        sleep(delay)
        if (time_ns()-start_time)*1e-9 > 31:
            running = False 


    sleep(30)
    driver.close()

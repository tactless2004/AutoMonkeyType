from time import sleep, time_ns
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains # Sends generic (non-element specific) actions

def get_words(driver: webdriver) -> iter:
    words = driver.find_elements(By.CSS_SELECTOR, "div.word")
    words_list = word.text for word in words
    print(words_list)
    return iter(words)

if __name__ == "__main__":
    # Argument Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("--wpm", help="The intended wpm you want to Auto-MonkeyType at.")
    args = parser.parse_args()
    if args.wpm:
        try:
            wpm = int(args.wpm)
        except ValueError:
            print("Please provide a valid wpm.")
            exit()
    else:
        wpm = 200
    delay = 60/wpm # This will never yield the intended wpm exactly, but its close.

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
    stop_time = 30 

    while running:
        try:
            word = next(word_iterator).text
            action.send_keys(word)
            action.send_keys(" ")
            action.perform()
            print(f"SENT: {word}")
        except StopIteration:
            word_iterator = get_words(driver)
            continue
        except Exception as e:
            # Generic Exception, usually the typing page is dead 
            print(f"{e}")
            running = False

        if (time_ns() - initial_time)*1e-9 > stop_time:
            running = False

        sleep(delay)

    sleep(3)
    driver.close()

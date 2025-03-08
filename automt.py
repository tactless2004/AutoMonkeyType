from time import sleep, time_ns
import argparse
from word_buffer import buf
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains # Sends generic (non-element specific) actions

def get_words(driver: webdriver, most_recent_three = None) -> iter:
    words = driver.find_elements(By.CSS_SELECTOR, "div.word")
    words_list = [word.text for word in words]
    if most_recent_three is None or len(most_recent_three) < 3:
        return iter(words_list)
    else:
        new_words_list = words_list[find_next_idx(words_list, most_recent_three):]
        return iter(new_words_list)

# Some already typed words, are still className="div.word", so we just find where the ones we've already typed end.
def find_next_idx(word_list: list, most_recent_three: list) -> int:
    l = 0
    r = 3
    for _ in range(0, len(word_list)-2):
        if word_list[l:r] == most_recent_three:
            return r
        else:
            l += 1
            r += 1
    return -1
            

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
        wpm = 400
    delay = 60/wpm # This will never yield the intended wpm exactly, but its close.

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
    stop_time = 30 
    three_buffer = buf()

    while running:
        try:
            word = next(word_iterator)
            action.send_keys(word)
            action.send_keys(" ")
            action.perform()
            three_buffer.add(word)

        except StopIteration:
            word_iterator = get_words(driver, three_buffer.get_words())
            continue
        except Exception as e:
            # Generic Exception, usually the typing page is dead 
            print(f"{e}")
            running = False

        # Check if its been > 30 seconds.
        if (time_ns() - initial_time)*1e-9 > stop_time:
            running = False

        sleep(delay)

    sleep(3)
    driver.close()

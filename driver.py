from time import sleep, time_ns
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains # Sends generic (non-element specific) actions

def get_words(driver: webdriver) -> iter:
    words = driver.find_elements(By.CSS_SELECTOR, "div.word")
    return iter(words)

def test_over(driver: webdriver) -> bool:
    words = driver.find_elements(By.CSS_SELECTOR, "div.word")
    if words == []:
        return True
    else: 
        return False

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


    initial_time = time_ns()
    running = True
    word_iterator = get_words(driver)
    action = ActionChains(driver)
    wpm = 100
    fudge = 20
    delay = (60/(wpm-fudge))
    
    while running:
        try:
            action.send_keys(next(word_iterator).text)
            action.send_keys(" ")
            action.perform()
        except StopIteration:
            word_iterator = get_words(driver)
        except Exception as e:
            # Generic Exception, usually the typing page is dead 
            print(f"{e}")
            running = False

        # print(f"Remaining Time: {(time_ns()-initial_time)*1e-9}s")

        if (time_ns() - initial_time)*1e-9 > 29.5:
            running = False
        if test_over(driver):
            print("test_over :(")

        sleep(delay)
    sleep(20)
    driver.close()

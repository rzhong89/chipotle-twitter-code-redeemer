import re
import time

import pyautogui
import selenium.common.exceptions
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import test

username = "xxx@gmail.com"
password = "123"
phone = '111111111'
twitter = 'USWNT'
keyword = 'text'
service = Service("chromedriver.exe")
tweets = []

options = webdriver.ChromeOptions()
options.add_extension(r'C:\Users\xxx\PycharmProjects\chipotleBot\OldTwitterChrome.zip')
driver = webdriver.Chrome(service=service, options=options)

def start():
    driver.get(f"https://twitter.com/{twitter}")
    time.sleep(3)
    #pyautogui.click(x=-370, y=423)
    try:
        element_present = EC.presence_of_element_located((By.NAME, 'text'))
        WebDriverWait(driver, 7).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")
    username_input = driver.find_element("name", "text")
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)

    time.sleep(5)

    if driver.find_element("name", "text"):
        phone_input = driver.find_element("name", "text")
        phone_input.send_keys(phone)
        phone_input.send_keys(Keys.RETURN)
        time.sleep(3)

    password_input = driver.find_element("name", "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)
    driver.get(f"https://twitter.com/{twitter}")
    time.sleep(1)

    pyautogui.click(x=991, y=1051)
    time.sleep(3)
    pyautogui.click(x=45, y=291)
    time.sleep(1)
    pyautogui.click(x=462, y=80)
    time.sleep(1)
    pyautogui.typewrite('888222')
    time.sleep(1)
    pyautogui.press("Enter")
    time.sleep(1)


def get_last_text():
    driver.refresh()
    try:
        element_present = EC.presence_of_element_located((By.XPATH, f'/html/body/main/div/div[2]/div[10]/div[1]/div[3]/span'))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded")
    last_tweet = driver.find_element(By.XPATH, f'/html/body/main/div/div[2]/div[10]/div[1]/div[3]/span')
    return last_tweet.text


def check_for_code(tweet):
    code = None
    if keyword.lower() in tweet.lower() and tweet not in tweets:
        tweets.append(tweet)
        pattern = re.compile(fr'{keyword.lower()} (\w+)', re.IGNORECASE)
        match = pattern.search(tweet)
        if match:
            code = match.group(1)
    return code


def text_code(code):
    pyautogui.typewrite(code)
    time.sleep(.01)
    pyautogui.press("Enter")


def master():
    start()
    goals = test.getUSAGoals()
    while not test.isFinished():
        current = test.getUSAGoals()
        if current > goals:
            goals = current
            for i in range(30):
                try:
                    tweet = get_last_text()
                    code = check_for_code(tweet)
                    if code is not None:
                        text_code(code)
                    time.sleep(3)
                except selenium.common.exceptions.NoSuchElementException:
                    print("Rate limit reached. Sleeping for 15 minutes.")
                    time.sleep(900)
                    break
        time.sleep(1)

start()
while True:
    try:
        tweet = get_last_text()
        code = check_for_code(tweet)
        if code is not None:
            text_code(code)
        time.sleep(3)
    except selenium.common.exceptions.NoSuchElementException:
        print("Rate limit reached. Sleeping for 15 minutes.")
        time.sleep(900)
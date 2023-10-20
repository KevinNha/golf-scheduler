from dotenv import load_dotenv
import os
import time

import utils.utils as utils
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webdriver import WebDriver # type

load_dotenv()

GOLF_WEBSITE = os.getenv("GOLF_WEBSITE")
COURSE_ID = "courseid1"

def login(driver: WebDriver, email: str, password: str) -> None:
    # Login button
    driver.find_element(By.XPATH, ".//button[@mat-button]").click()

    email_input_element = driver.find_element(By.NAME, "email")
    email_input_element.send_keys(email)
    email_input_element.send_keys(Keys.ENTER)
    password_input_element = driver.find_element(By.NAME, "password")
    password_input_element.send_keys(password)
    sign_in_button = driver.find_element(By.XPATH, ".//button[@type='submit']")

    sign_in_button.click()

def pick_last_date_from_calendar(driver: WebDriver) -> None:
    while True:
        try:
            all_calendar_elements = driver.find_elements(By.XPATH, './/span[@class = "day-background-upper is-visible"]')
            all_calendar_elements[-1].click()
            break
        except:
            print("Calendar not loaded yet yet")

def acknowledge(driver: WebDriver) -> None:
    max_timeout = 30
    start_time = time.time()
    while time.time() - start_time < max_timeout:
        try:
            acknowledgementButton = driver.find_element(By.XPATH, './/button[@class = "mat-focus-indicator full-width btn-action mat-raised-button mat-button-base mat-primary"]')
            if (acknowledgementButton.is_enabled()):
                acknowledgementButton.click()
                break
        except:
            time.sleep(0.1)

def reserve(driver: WebDriver) -> None:
    max_timeout = 30
    start_time = time.time()
    while time.time() - start_time < max_timeout:
        try:
            reserve_button = driver.find_element(By.CLASS_NAME, "button-section").find_element(By.TAG_NAME, "button")
            if (reserve_button.is_enabled()):
                reserve_button.click()
                print("Successfully reserved!")
                break
        except:
            time.sleep(0.1)

def register(tee_start_time: int, tee_end_time: int, email: str, password: str):
    driver = webdriver.Chrome()
    driver.implicitly_wait(25) # This is an arbitrary number - can be changed depending on use-case

    driver.get(GOLF_WEBSITE.format(tee_start_time,tee_end_time))
    driver.maximize_window()

    login(driver, email, password)
    utils.wait_until_registration()
    driver.refresh()    

    pick_last_date_from_calendar(driver)
    
    tee_times_length = -1
    while True:
        tee_times = driver.find_elements(By.CLASS_NAME, f"teetimeitem-{COURSE_ID}")
        if (len(tee_times) == 0):
            print("Failed to reserve.")
            break

        if (len(tee_times) == tee_times_length):
            print("Tee times not update rendered yet.")
            continue

        if (tee_times_length == -1):
            time.sleep(5)
        tee_times_length = len(tee_times)

        # Choosing the second item because the first one is likely to be more popular
        tee_times[0].find_element(By.CLASS_NAME, "btnStepper").click()
        try:
            no_longer_available_popup = driver.find_element(By.ID, 'cdk-overlay-0')
            if (no_longer_available_popup):
                print("Looks like someone already booked it.")
                no_longer_available_popup.find_element(By.TAG_NAME, 'button').click()
                continue
        except Exception as e:
            break

    acknowledge(driver)
    reserve(driver)

    time.sleep(10)
    driver.quit()

def main():
    tee_start_time, tee_end_time, email, password = utils.get_user_inputs()
    register(tee_start_time, tee_end_time, email, password)

if __name__ == '__main__':
    main()
    
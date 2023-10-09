from datetime import datetime
from dotenv import load_dotenv
import os
import time

import utils.gui_inputs as gui
import pytz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

load_dotenv()

GOLF_WEBSITE = os.getenv("GOLF_WEBSITE")
GOLF_RESERVATION_SITE = os.getenv("GOLF_RESERVATION_SITE")
COURSE_ID = "courseid1"

def get_user_inputs():
    tee_start_time = gui.get_tee_start_time_range()
    if (tee_start_time == None):
        raise Exception("Invalid tee time")
    
    tee_end_time = gui.get_tee_end_time_range(tee_start_time)
    if (tee_end_time == None):
        raise Exception("Invalid tee time")

    email, password = gui.get_login_information()

    return (tee_start_time, tee_end_time, email, password)

def wait_until_registration():
    target_time_format = "%I:%M:%S %p %Z"

    target_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 12, 0, 1)

    pacific_tz = pytz.timezone("America/Los_Angeles")
    target_time_pst = pacific_tz.localize(target_time)

    print("Check time: ", target_time_pst.strftime(target_time_format))

    while datetime.now(pacific_tz) <= target_time_pst:
        current_time = datetime.now(pacific_tz)
        print("Current time: ", current_time.strftime(target_time_format))
        print("Waiting for the target time...")
        time.sleep(1)

    print("Current time: ", current_time.strftime(target_time_format))
    print("Target time reached!")

def register(tee_start_time: int, tee_end_time: int, email: str, password: str):
    driver = webdriver.Chrome()
    driver.implicitly_wait(25)

    driver.get(GOLF_WEBSITE.format(tee_start_time,tee_end_time))
    driver.maximize_window()

    # Login button
    driver.find_element(By.XPATH, ".//button[@mat-button]").click()

    # Login
    email_input_element = driver.find_element(By.NAME, "email")
    email_input_element.send_keys(email)
    email_input_element.send_keys(Keys.ENTER)
    password_input_element = driver.find_element(By.NAME, "password")
    password_input_element.send_keys(password)
    sign_in_button = driver.find_element(By.XPATH, ".//button[@type='submit']")

    wait_until_registration()
    sign_in_button.click()

    # Chooses the last day in calendar
    while True:
        try:
            all_calendar_elements = driver.find_elements(By.XPATH, './/span[@class = "day-background-upper is-visible"]')
            all_calendar_elements[-1].click()
            break
        except:
            print("Calendar not loaded yet yet")
    
    tee_time_ids = []
    tee_times = driver.find_elements(By.CLASS_NAME, f"teetimeitem-{COURSE_ID}")
    print(tee_times)
    for tee_time in tee_times:
        tee_time_card = tee_time.find_element(By.CLASS_NAME, "teetimecard")
        tee_time_ids.append(tee_time_card.get_attribute('id').split("-")[1])
    print(tee_time_ids)

    max_timeout = 20
    for id in tee_time_ids:
        reserved = False
        try:
            driver.get(GOLF_RESERVATION_SITE.format(id))
        except:
            print("Reservation no longer available")
            continue

        start_time = time.time()
        while time.time() - start_time < max_timeout:
            try:
                reserve_button = driver.find_element(By.CLASS_NAME, "button-section").find_element(By.TAG_NAME, "button")
                if (reserve_button.is_enabled()):
                    reserve_button.click()
                    time.sleep(60)
                    reserved = True
                    break
            except Exception as e:
                print("reservation button not clickable")
                time.sleep(0.5)

        if (reserved):
            print("Reservation complete!")
            break
        else:
            print("Failed to reserve")

def main():
    tee_start_time, tee_end_time, email, password = get_user_inputs()
    register(tee_start_time, tee_end_time, email, password)

if __name__ == '__main__':
    main()
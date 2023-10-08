from datetime import datetime
from dotenv import load_dotenv
import os
import time

import easygui
import pytz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

load_dotenv()

TARGET_DATE_FORMAT = "%m-%d-%Y"
GOLF_WEBSITE = os.getenv("GOLF_WEBSITE")
GOLF_RESERVATION_SITE = os.getenv("GOLF_RESERVATION_SITE")

def get_user_inputs():
    title = "Golf Registration Tee Start Time"
    msg = "Tee 시작 시간의 시작 범위를 입력해주세요. 자연수를 입력 해야하며 5 (오전 5시) 부터 22 (오후 10시) 까지 가능합니다."
    default = 5
    lowerbound = 5
    upperbound = 22
    tee_start_time = easygui.integerbox(msg, title, default, lowerbound, upperbound)
    
    if (tee_start_time == None):
        raise Exception("Invalid tee time")
    
    title = "Golf Registration Tee End Time"
    msg = "Tee 시작 시간의 끝 범위를 입력해주세요. 자연수를 입력 해야하며 시작 범위 ({}) 부터 23 (오후 11시) 까지 가능합니다.".format(tee_start_time)
    default = tee_start_time
    lowerbound = tee_start_time
    upperbound = 23
    tee_end_time = easygui.integerbox(msg, title, default, lowerbound, upperbound)
    
    if (tee_end_time == None):
        raise Exception("Invalid tee time")

    msg = "로그인 정보를 입력해주세요."
    title = "Golf Registration Login"
    fieldNames = ["User Email", "Password"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = easygui.multpasswordbox(msg, title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues is None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = easygui.multpasswordbox(errmsg, title, fieldNames, fieldValues)

    return (tee_start_time, tee_end_time, fieldValues[0], fieldValues[1])

def wait_until_registration():
    target_time_format = "%I:%M:%S %p %Z"

    target_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 12, 0, 0)

    # Define PST timezone
    pacific_tz = pytz.timezone("America/Los_Angeles")

    # Localize the target time to PST timezone
    target_time_pst = pacific_tz.localize(target_time)

    print("Check time (12:00 PM PST): ", target_time_pst.strftime(target_time_format))

    # Continuously check if the current time is greater than or equal to the target time
    while datetime.now(pacific_tz) <= target_time_pst:
        current_time = datetime.now(pacific_tz)
        print("Current time:", current_time.strftime(target_time_format))
        print("Waiting for the target time...")
        time.sleep(1)  # Wait for 1 second before checking again

    print("Current time:", current_time.strftime(target_time_format))
    print("Target time reached!")


def register(tee_start_time: int, tee_end_time: int, email: str, password: str):
    driver = webdriver.Chrome()
    driver.implicitly_wait(25)

    driver.get(GOLF_WEBSITE.format(tee_start_time,tee_end_time))

    # Login button
    driver.find_element(By.XPATH, ".//button[@mat-button]").click()

    # Login
    email_input_element = driver.find_element(By.NAME, "email")
    email_input_element.send_keys(email)
    email_input_element.send_keys(Keys.ENTER)
    password_input_element = driver.find_element(By.NAME, "password")
    password_input_element.send_keys(password)
    signin_button = driver.find_element(By.XPATH, ".//button[@type='submit']")
    signin_button.click()

    # Chooses the last day in calendar
    while True:
        try:
            all_calendar_elements = driver.find_elements(By.XPATH, './/span[@class = "day-background-upper is-visible"]')
            all_calendar_elements[-1].click()
            break
        except:
            print("Calendar not loaded yet yet")
    
    # courseid1 is burnaby, courseid2 is riverway
    tee_time_ids = []
    tee_times = driver.find_elements(By.CLASS_NAME, "teetimeitem-courseid1")
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
    wait_until_registration()
    register(tee_start_time, tee_end_time, email, password)

if __name__ == '__main__':
    main()
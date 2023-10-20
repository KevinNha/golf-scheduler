from datetime import datetime
import time

import utils.gui_inputs as gui
import pytz

def get_user_inputs() -> list[int | str]:
    tee_start_time = gui.get_tee_start_time_range()
    if (tee_start_time == None):
        raise Exception("Invalid tee time")
    
    tee_end_time = gui.get_tee_end_time_range(tee_start_time)
    if (tee_end_time == None):
        raise Exception("Invalid tee time")

    email, password = gui.get_login_information()

    return (tee_start_time, tee_end_time, email, password)

def wait_until_registration() -> None:
    target_time_format = "%I:%M:%S %p %Z"

    target_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 12, 0, 0)

    pacific_tz = pytz.timezone("America/Los_Angeles")
    target_time_pst = pacific_tz.localize(target_time)

    print("Check time: ", target_time_pst.strftime(target_time_format))

    while datetime.now(pacific_tz) < target_time_pst:
        current_time = datetime.now(pacific_tz)
        print("Current time: ", current_time.strftime(target_time_format))
        print("Waiting for the target time...")
        time.sleep(0.2)

    print("Current time: ", current_time.strftime(target_time_format))
    print("Target time reached!")
    
import easygui

def get_tee_start_time_range() -> int:
    title = "Golf Registration Tee Start Time"
    msg = "Tee 시작 시간의 시작 범위를 입력해주세요. 자연수를 입력 해야하며 5 (오전 5시) 부터 22 (오후 10시) 까지 가능합니다."
    default = 5
    lower_bound = 5
    upper_bound = 22
    return easygui.integerbox(msg, title, default, lower_bound, upper_bound)

def get_tee_end_time_range(tee_start_time: int) -> int:
    title = "Golf Registration Tee End Time"
    msg = "Tee 시작 시간의 끝 범위를 입력해주세요. 자연수를 입력 해야하며 시작 범위 ({}) 부터 23 (오후 11시) 까지 가능합니다.".format(tee_start_time)
    default = tee_start_time
    lower_bound = tee_start_time
    upper_bound = 23
    return easygui.integerbox(msg, title, default, lower_bound, upper_bound)

def get_login_information() -> list:
    msg = "로그인 정보를 입력해주세요."
    title = "Golf Registration Login"
    fieldNames = ["User Email", "Password"]
    fieldValues = []
    fieldValues = easygui.multpasswordbox(msg, title, fieldNames)

    # make sure that none of the fields was left blank
    while True:
        if fieldValues is None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": break
        fieldValues = easygui.multpasswordbox(errmsg, title, fieldNames, fieldValues)
 
    return [fieldValues[0], fieldValues[1]]
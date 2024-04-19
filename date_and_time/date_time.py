from datetime import datetime

def current_time():
    current_time = datetime.now().time()
    formatted_time = "{:02d}:{:02d}:{:02d}".format(current_time.hour, current_time.minute, current_time.second)
    return formatted_time

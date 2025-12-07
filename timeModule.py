from datetime import datetime
import pytz
def get_time_ist():
    ist = pytz.timezone("Asia/Kolkata")
    current_time = datetime.now(ist)
    return current_time.strftime("The time is %I:%M %p")

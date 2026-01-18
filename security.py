import pytz
from datetime import datetime
from config import PASSWORD_PREFIX, TIMEZONE

tz = pytz.timezone(TIMEZONE)

def get_password():
    t = datetime.now(tz).strftime("%H%M")
    return PASSWORD_PREFIX + t

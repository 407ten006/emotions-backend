from datetime import datetime

from dateutil import tz


def utc_now():
    return datetime.utcnow().replace(tzinfo=tz.tzutc())

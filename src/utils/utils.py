from datetime import datetime

from dateutil import tz


def utc_now():
    return datetime.utcnow().replace(tzinfo=tz.tzutc())


def kst_now():
    return datetime.now().replace(tzinfo=tz.tzlocal())


def kst_today_yymmdd():
    return kst_now().strftime("%Y%m%d")

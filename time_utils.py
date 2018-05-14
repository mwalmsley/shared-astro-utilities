import datetime


def current_time():
    return datetime.datetime.now().time()


def current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

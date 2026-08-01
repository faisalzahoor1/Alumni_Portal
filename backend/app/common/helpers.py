
from datetime import datetime


def utc_now():

    return datetime.utcnow()

def build_full_name(first, last):

    return f"{first} {last}"
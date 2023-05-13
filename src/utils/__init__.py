import random
import string

from enums import Interval
from uuid import uuid4


# generate random unique digit
def generate_random_digit(length: int):
    return "".join(random.choice(string.digits) for _ in range(length))


# Generate strong random unique string
def generate_random_string(length: int):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_uuid():
    return uuid4().hex


# Convert interval to seconds
def interval_to_seconds(interval: Interval) -> int:
    """Convert interval to seconds

    :param interval: The interval

    :return: The interval in seconds

    :rtype: int
    """
    if interval == Interval.MINUTE_1:
        return 60
    elif interval == Interval.MINUTE_3:
        return 60 * 3
    elif interval == Interval.MINUTE_5:
        return 60 * 5
    elif interval == Interval.MINUTE_15:
        return 60 * 15
    elif interval == Interval.MINUTE_30:
        return 60 * 30
    elif interval == Interval.HOUR_1:
        return 60 * 60
    elif interval == Interval.HOUR_2:
        return 60 * 60 * 2
    elif interval == Interval.HOUR_4:
        return 60 * 60 * 4
    elif interval == Interval.HOUR_6:
        return 60 * 60 * 6
    elif interval == Interval.HOUR_8:
        return 60 * 60 * 8
    elif interval == Interval.HOUR_12:
        return 60 * 60 * 12
    elif interval == Interval.DAY_1:
        return 60 * 60 * 24
    elif interval == Interval.DAY_3:
        return 60 * 60 * 24 * 3
    elif interval == Interval.WEEK_1:
        return 60 * 60 * 24 * 7
    elif interval == Interval.MONTH_1:
        return 60 * 60 * 24 * 30
    else:
        raise ValueError("Invalid interval")

"""
Some time intervals in seconds.
"""
from typing import NewType

Interval = NewType('Interval', int)

MINUTE: Interval = 60
HOUR: Interval = MINUTE * 60
SIXHOURS: Interval = HOUR * 6
TWELVEHOURS: Interval = HOUR * 12
DAY: Interval = HOUR * 24
WEEK: Interval = DAY * 7

intervals = [MINUTE, HOUR, SIXHOURS, TWELVEHOURS, DAY, WEEK]

def intervalToString(interval: Interval):
    if interval == 60: return "minute"
    elif interval == 60 * 60: return "hour"
    elif interval == 60*60*12: return "12 hours"
    elif interval == 60*60*24: return "day"
    else: return "week"


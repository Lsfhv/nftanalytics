"""
Some time intervals in seconds.
"""
from typing import NewType

Interval = NewType('Interval', int)

MINUTE: Interval = Interval(60)
HOUR: Interval = Interval(60 * MINUTE)
SIXHOURS: Interval = Interval(HOUR * Interval(6))
TWELVEHOURS: Interval = Interval(HOUR * Interval(12))
DAY: Interval = Interval(HOUR * Interval(24))
WEEK: Interval = Interval(DAY * Interval(7))
MONTH: Interval = Interval(WEEK * Interval(4))

intervals: list[Interval] = [MINUTE, HOUR, SIXHOURS, TWELVEHOURS, DAY, WEEK]

def intervalToString(interval: Interval) -> str:
    if interval == 60: return "minute"
    elif interval == 60 * 60: return "hour"
    elif interval == 60*60*12: return "12 hours"
    elif interval == 60*60*24: return "day"
    else: return "week"


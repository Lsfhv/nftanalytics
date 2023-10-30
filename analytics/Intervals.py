"""
Some time intervals in seconds.
"""
from typing import NewType

Interval = NewType('Interval', int)

MINUTE: Interval = Interval(60)
FIFTEENMINUTES: Interval = Interval(MINUTE * 15)
HOUR: Interval = Interval(60 * MINUTE)
SIXHOURS: Interval = Interval(HOUR * Interval(6))
TWELVEHOURS: Interval = Interval(HOUR * Interval(12))
DAY: Interval = Interval(HOUR * Interval(24))
WEEK: Interval = Interval(DAY * Interval(7))
MONTH: Interval = Interval(WEEK * Interval(4))

intervals: list[Interval] = [FIFTEENMINUTES]

def intervalToString(interval: Interval) -> str:
    if interval == MINUTE: return '1m'
    elif interval == FIFTEENMINUTES: return '15m'
    elif interval == HOUR: return '1H'
    elif interval == DAY: return '1D'
    elif interval == WEEK: return '1W'
    else: return '1M'

def stringToInterval(s: str) -> Interval:
    if s == '1m': return MINUTE
    if s == '15m': return FIFTEENMINUTES
    elif s == '1H': return HOUR
    elif s == '1D': return DAY
    elif s == '1W': return WEEK
    else: return MONTH



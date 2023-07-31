"""
Some time intervals in seconds.
"""

MINUTE = 60
HOUR = MINUTE * 60
SIXHOURS = HOUR * 6
TWELVEHOURS = HOUR * 12
DAY = HOUR * 24
WEEK = DAY * 7

intervals = [MINUTE, HOUR, SIXHOURS, TWELVEHOURS, DAY, WEEK]

def intervalToString(interval):
    if interval == 60: return "minute"
    elif interval == 60 * 60: return "hour"
    elif interval == 60*60*12: return "12 hours"
    elif interval == 60*60*24: return "day"
    else: return "week"


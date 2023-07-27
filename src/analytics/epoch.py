"""
Some calculations with epoch time.
"""

"""
How many (seconds/hours/day) between startTime and endTime
"""
def epochToX(startTime, endTime, format=None):
    if endTime < startTime: 
        print("End time is before start time, returning null")
        return None
    
    relative = endTime - startTime

    if format == None: return relative
    elif format == "HOUR": return relative / (60 * 60)
    elif format == "DAY": return relative / (60 * 60 * 24)
    elif format == "WEEK": return relative / (60 * 60 * 24 * 7)
    else:
        print("Bad format specified, returning null")
        return None
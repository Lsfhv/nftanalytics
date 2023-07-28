"""
How many listings were created in the path (HOUR/DAY/WEEK)
"""

from analytics.numberListed import getAllListings
from time import time


"""
How many listings have been listing in past [...]
"""
def listedInPast(interval, slug):
    listings = getAllListings(slug)

    startTimes = list(map(lambda x : int(x['startTime']), listings))

    currentTime = time()

    bound = currentTime - interval
    
    result = 0
    for i in startTimes:
        if i >= bound:
            result += 1

    return result
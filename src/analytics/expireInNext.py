"""
Compute how many were listed between.
"""

from analytics.collection import getAllListings
from analytics.epoch import epochToX
from time import time


"""
How many listing will expire in next (HOUR/DAY/WEEK)
"""
def expireInNext(interval, slug):

    startTime = time()
    bound = 1

    listingEndTimes = list(map(lambda x : int(x['endTime']),getAllListings(slug)))

    listingEndTimes = list(map(lambda x : epochToX(startTime, x, interval),listingEndTimes))


    listingEndTimes.sort()

    result = listingEndTimes
    for i in range(0, len(listingEndTimes)):
        if not listingEndTimes[i] <= bound:
            result = listingEndTimes[:i]
            break            

    return len(result)
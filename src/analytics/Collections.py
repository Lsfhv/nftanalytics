"""Tracks the amount of items listed 
within past day/week/month.
"""

from request.getRequest import get
from time import time

from Postgresql import PostgresConnection
from Intervals import intervals, Interval

from datetime import datetime
from sql.sqlQGenerator import insertG, updateG
from time import sleep
from Keys import openseaBaseEndpointV1, openseaBaseEndpointV2, openseaHeaders
from Intervals import HOUR, MINUTE, FIFTEENMINUTES
import asyncio
from analytics.Transfers import monitorTransfers
from analytics.Volume import computeVolume

class Collection:

    retrieveAllListingsOS = lambda slug: f"listings/collection/{slug}/all"
    retrieveStatsOS = lambda slug: f"collection/{slug}/stats"

    limit = "50"
    timer = 0

    lastUpdated = None # Time of last update in epoch time

    uniqueListings = None
    stats = None
    listedInPastX = None
    
    def __init__(self, slug: str, address, chain='ethereum'):
        self.slug: str = slug
        self.address: str = address.lower()
        self.chain: str = chain
        self.delay: Interval = HOUR
        
        if (not self.existsInDB()):
            self.refresh()
            sql = insertG('collections', self.toCollections())
            PostgresConnection().insert(sql)

    """
    Deletes entries in analytics after a certain amount of time.
    """
    def clean(self):
        PostgresConnection().insert(f"delete from analytics where last_updated <= {Collection.lastUpdated - 60*60*24*7*4} and address='{self.address}'")

    async def start(self):
        """
        Starts the coroutines that read moniter the chain.
        """

        asyncio.create_task(monitorTransfers(self.address))

        await asyncio.sleep(FIFTEENMINUTES)

        asyncio.create_task(computeVolume(self.address))
        # while True:
        #     self.refresh()
            
        #     PostgresConnection().insert(updateG('collections', ("address", self.address), self.toUpdateCollections()))

        #     sql = insertG('analytics', self.toAnalytics())
        #     PostgresConnection().insert(sql)
        #     self.clean()
            
        #     await asyncio.sleep(self.delay)


    # Data to be updated on the collections table.
    def toUpdateCollections(self):
        return [
            ('floor', self.stats['floor_price']), 
            ('total_listed', len(self.uniqueListings)),
            ('total_supply', self.stats['total_supply']),
            ('last_updated', self.lastUpdated)
        ]
    
    """
    Returns all the data that will be posted to DB on first time this collection is monitored.
    """
    def toCollections(self):
        return [
            self.address, 
            self.slug,
            self.chain,
            self.stats['floor_price'],
            len(self.uniqueListings),
            self.stats['total_supply'],
            self.lastUpdated
        ]
        
    # Data to be posted to analytics table.
    def toAnalytics(self):
        return [
            self.address, 
            self.stats['floor_price'],
            len(self.uniqueListings),
            Collection.listedInPastX[0],
            Collection.listedInPastX[1],
            Collection.listedInPastX[2],
            Collection.listedInPastX[3],
            Collection.listedInPastX[4],
            Collection.listedInPastX[5],
            Collection.lastUpdated, 
            self.stats['num_owners']
        ]
           
    # Refresh the data.
    def refresh(self):
        Collection.lastUpdated = time()
        Collection.uniqueListings = self.getUniqueListings()
        Collection.stats = self.getStats()
        Collection.listedInPastX = self.getListedInPastX()

    def getStats(self):
        endpoint = Collection.retrieveStatsOS(self.slug)
        return get(openseaBaseEndpointV1, endpoint, headers = openseaHeaders).json()['stats']
    
    """
    Returns all listings. 
    It can be the case that there are multiple listings for a single nft.
    """
    def getAllListings(self):
        endpoint = Collection.retrieveAllListingsOS(self.slug)
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Getting all listings for {self.slug} [{dt_string}]... ")

        items = []

        params = {"limit": Collection.limit}
        response =  get(openseaBaseEndpointV2, endpoint, params = params, headers = openseaHeaders).json()    

        while 'next' in response:
            items += response['listings']

            params['next'] = response['next']
            response = get(openseaBaseEndpointV2, endpoint, params = params, headers = openseaHeaders).json()

        response = response['listings']
        items += response

        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Finished getting all listings for {self.slug} [{dt_string}]")

        return items
    
    """
    Filters result from getAllListings for the newest unique listing for each listed nft.
    """
    def getUniqueListings(self):
        listings = self.getAllListings()

        seen = set()
        result = []
        for i in range(len(listings) - 1, -1, - 1):
            currentListing = listings[i]
            currentId = listings[i]['protocol_data']['parameters']['offer'][0]['identifierOrCriteria']
            if currentId not in seen:
                seen.add(currentId)
                result.append(listings[i])

        return result
    
    """
    How many listings were made in the past [...]
    """
    def getListedInPastX(self):
        listings = self.uniqueListings
        startTimes = list(map(lambda x : int(x['protocol_data']['parameters']['startTime']), listings))
        startTimes.sort(reverse = True)
        currentTime = time()

        result = []
        pointer = 0
        for i in range(0, len(intervals)):
            bound = currentTime - intervals[i]
            
            while pointer < len(startTimes):
                if startTimes[pointer] >= bound:
                    pointer += 1
                else:
                    break
            result.append(pointer)
                    
        return result
    
    # Check if this collection exists in the collections table.
    def existsInDB(self) -> bool:
        response = PostgresConnection().readonly(f"select 1 from collections where slug='{self.slug}'")
        
        if len(response) == 0:
            return False
        else: 
            if response[0][0] == 1: 
                return True
        return False
    
    def processTransfers(self, queue):
        pass
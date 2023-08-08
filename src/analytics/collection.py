"""Tracks the amount of items listed 
within past day/week/month.
"""

from request.getRequest import get
from time import time

from postgresconnection import PostgresConnection
from intervals import intervals

from datetime import datetime
from sql.sqlQGenerator import insertG, updateG
from time import sleep

class Collection:

    retrieveAllListings = lambda slug: f"listings/collection/{slug}/all"
    retrieveStats = lambda slug: f"collection/{slug}/stats"

    limit = "50"
    timer = 0

    lastUpdated = None # Time of last update in epoch time

    uniqueListings = None
    stats = None
    listedInPastX = None
    

    def __init__(self, slug, address, chain='ethereum'):
        self.slug = slug
        self.address = address.lower()
        self.chain = chain

        if (not self.existsInDB()):
            self.refresh()
            sql = insertG('collections', self.toCollections())
            PostgresConnection().insert(sql)

    def start(self):
        while True:
            self.refresh()
            
            sql = insertG('analytics', self.toAnalytics())
            PostgresConnection().insert(sql)
            sleep(60 * 1)
    
    """
    Returns all the data that will be posted to DB.
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
            Collection.lastUpdated
        ]
           
    def refresh(self):
        Collection.lastUpdated = time()
        Collection.uniqueListings = self.getUniqueListings()
        Collection.stats = self.getStats()
        Collection.listedInPastX = self.getListedInPastX()

    def getStats(self):
        endpoint = Collection.retrieveStats(self.slug)
        return get(endpoint)['stats']
    
    """
    Returns all listings. 
    It can be the case that there are multiple listings for a single nft.
    """
    def getAllListings(self):
        endpoint = Collection.retrieveAllListings(self.slug)
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Getting all listings for {self.slug} [{dt_string}]... ")

        items = []

        params = {"limit": Collection.limit}
        response =  get(endpoint, v2 = True, params = params)    

        while 'next' in response:
            items += response['listings']

            params['next'] = response['next']
            response = get(endpoint, v2 = True, params = params)

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
    
    """
    Checks if this collection already exists in the db. 
    If it does then it checks if hasnt been updated recently.
    Return false means that the api will be called and db will be updated.
    Return true means that db wont be updated as it was already updated recently (Recently meaning 5 minutes).
    """
    def existsInDBAndBeenUpdatedInPastXMins(self):
        response = PostgresConnection().readonly(f"select last_updated from collections where slug = '{self.slug}'")
        if len(response) == 0: return False
        else:
            lastUpdated = response[0][0]
            currentTime = time()

            if (lastUpdated == None) or (lastUpdated + (60 * Collection.timer) <= currentTime):
                return False
            return True

    def existsInDB(self):
        response = PostgresConnection().readonly(f"select 1 from collections where slug='{self.slug}'")
        
        if len(response) == 0:
            return False
        else: 
            if response[0][0] == 1: 
                return True
        return False
    
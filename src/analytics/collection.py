"""Tracks the amount of items listed 
within past day/week/month.
"""

from request.getRequest import get
from time import time
# from src.postgresconnection import PostgresConnection
from postgresconnection import PostgresConnection

class Collection:

    # https://docs.opensea.io/reference/retrieve-all-listings
    retrieveAllListings = lambda slug: f"listings/collection/{slug}/all"
    stats = lambda slug: f"collection/{slug}/stats"
    limit = "50"
    lastUpdated = None

    def __init__(self, slug, address):
        self.slug = slug
        self.address = address

        self.existsInDB()

        # if not self.existsInDBAndBeenUpdatedInPastXMins():
        #     floorPrice = self.getFloor()


        # PostgresConnection().readonly(f"")

        # self.uniqueListings = self.getUniqueListings()

        # self.numberOfListings = len(self.uniqueListings)

    def getFloor(self):
        endpoint = Collection.stats(self.slug)
        return get(endpoint)['stats']['floor_price']

    """
    Returns all listings. 
    It can be the case that there are multiple listings for a single nft.
    """
    def getAllListings(self):
        endpoint = Collection.retrieveAllListings(self.slug)

        print(f"Getting all listings for {self.slug} ... ")

        items = []

        params = {"limit": Collection.limit}
        response =  get(endpoint, v2 = True, params = params)    

        while 'next' in response:
            items += response['listings']

            params['next'] = response['next']
            response = get(endpoint, v2 = True, params = params)

        response = response['listings']
        items += response

        print(f"Finished getting all listings for {self.slug}")

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
    def listedInPast(self, interval):
        listings = self.uniqueListings
        startTimes = list(map(lambda x : int(x['protocol_data']['parameters']['startTime']), listings))

        currentTime = time()

        bound = currentTime - interval
        
        result = 0
        for i in startTimes:
            if i >= bound:
                result += 1

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

            if (lastUpdated == None) or (lastUpdated + (60 * 5) <= currentTime) :
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
        

        


# LIMIT = "50"
# HOUR = "HOUR"


# """
# Gets the total nft count for a collection.
# https://docs.opensea.io/v1.0/reference/retrieving-collection-stats
# """
# def getTotalItems(slug):
#     url = f"collection/{slug}/stats"
#     return get(url)['stats']['total_supply']

# """
# https://docs.opensea.io/reference/retrieve-nfts-by-contract

# Returns a list of token ids.
# """
# def getIds(address, chain):
#     endpoint = f"""chain/{chain}/contract/{address}/nfts"""

#     params = {"limit": LIMIT}

#     response = get(endpoint, v2 = True, params = params)
#     items =[]
#     print("Getting nft ids ... ")
#     while 'next' in response:
#         items += list(map(lambda x: int(x['identifier']), response['nfts']))

#         params['next'] = response['next']
#         response = get(endpoint, v2 = True, params = params)   

#     items += list(map(lambda x: int(x['identifier']), response['nfts']))

#     print("Finished")

#     return items

# """
# Returns all listings. 
# It can be the case that there are multiple listings for a single nft.
# """
# def getAllListings(slug):
#     endpoint = f"listings/collection/{slug}/all"

#     print(f"Getting all listings for {slug} ... ")

#     items = []
#     params = {"limit":LIMIT}
#     response =  get(endpoint, v2 = True, params = params)    

#     while 'next' in response:
#         items += response['listings']

#         params['next'] = response['next']
#         response = get(endpoint, v2 = True, params = params)

#     response = response['listings']
#     items += response

#     print(f"Finished getting all listings for {slug}")

#     return items

# """
# Gets the newest listing for each nft.
# """
# def getUniqueListings(slug):
#     listings = getAllListings(slug)

#     seen = set()
#     result = []
#     for i in range(len(listings) - 1, -1, - 1):
#         currentListing = listings[i]
#         currentId = listings[i]['protocol_data']['parameters']['offer'][0]['identifierOrCriteria']
#         if currentId not in seen:
#             seen.add(currentId)
#             result.append(listings[i])

#     return result

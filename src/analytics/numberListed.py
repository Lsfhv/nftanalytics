"""Tracks the amount of items listed 
within past day/week/month.
"""

from request.getRequest import get
from analytics.epoch import epochToX
from time import time


LIMIT = "50"
HOUR = "HOUR"

"""
https://docs.opensea.io/reference/retrieve-nfts-by-contract

Returns a list of token ids.
"""
def getIds(address, chain):
    endpoint = f"""chain/{chain}/contract/{address}/nfts"""

    params = {"limit": LIMIT}

    response = get(endpoint, v2 = True, params = params)
    items =[]
    print("Getting nft ids ... ")
    while 'next' in response:
        items += list(map(lambda x: int(x['identifier']), response['nfts']))

        params['next'] = response['next']
        response = get(endpoint, v2 = True, params = params)   

    items += list(map(lambda x: int(x['identifier']), response['nfts']))

    print("Finished")

    return items

"""
Gets the listings by tokenIds
"""
def getListings(tokenIds, chain, address):
    endpoint = f"""orders/{chain}/seaport/listings?asset_contract_address={address}"""

    rst = ""

    for tokenId in tokenIds:
        rst += f"&token_ids={tokenId}"
    endpoint += rst

    response = get(endpoint, v2 = True)['orders']

    return response    


"""
Returns all listings.
"""
def getAllListings(slug):
    endpoint = f"listings/collection/{slug}/all"

    print(f"Getting all listings for {slug} ... ")

    items = []
    params = {"limit":LIMIT}
    response =  get(endpoint, v2 = True, params = params)

    s = set()
    

    while 'next' in response:
        
        r = response['listings']
        for i in r:
            s.add(i['protocol_data']['parameters']['offer'][0]['identifierOrCriteria'])
        items += list(map(lambda x: x['protocol_data']['parameters'], r))

        params['next'] = response['next']
        response = get(endpoint, v2 = True, params = params)

    response = response['listings']
    items += list(map(lambda x : x['protocol_data']['parameters'], response))

    print(f"Finished getting all listings for {slug}")

    return items


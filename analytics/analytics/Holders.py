import os
import requests
from Keys import infuraNftApi

def computeUniqueOwners(address: str) -> int:
    """Computes the number of unique owners for given address

    Args:
        address (str): contract address

    Returns:
        int: how many unique owners there are
    """
    response = requests.get(infuraNftApi(address), auth = (os.environ["INFURAKEY"], os.environ["INFURASECRET"])).json()
    cursor = response['cursor']
    owners = set()
    for i in response['owners']:
        owners.add(i['ownerOf'])
        
    while cursor != None:
        response = requests.get(infuraNftApi(address)+f"?cursor={cursor}", auth= (os.environ["INFURAKEY"], os.environ["INFURASECRET"])).json()
        cursor = response['cursor']
        for i in response['owners']:
            owners.add(i['ownerOf'])

    return len(owners)

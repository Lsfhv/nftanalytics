import os
from Keys import infuraNftApi
from request.getRequest import get
from Intervals import FIFTEENMINUTES, HOUR, DAY, WEEK

async def computeUniqueOwners(address: str) -> int:
    """Computes the number of unique owners for given address

    Args:
        address (str): contract address 

    Returns:
        int: how many unique owners there are
    """

    response = get(infuraNftApi(address), auth = (os.environ["INFURAKEY"], os.environ["INFURASECRET"])).json()
    cursor = response['cursor']

    owners = {i['ownerOf'] for i in response['owners']}
    
    while cursor != None:
        response = get(infuraNftApi(address), params={'cursor': cursor}, auth = (os.environ["INFURAKEY"], os.environ["INFURASECRET"])).json()

        cursor = response['cursor']
        owners = owners | {i['ownerOf'] for i in response['owners']}
    
    return len(owners)
        
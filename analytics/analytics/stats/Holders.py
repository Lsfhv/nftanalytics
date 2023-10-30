import os
from Keys import openseaBaseEndpointV2, openseaGetCollectionStats, openseaHeaders
from request.getRequest import get
from Postgresql import PostgresConnection

def computeUniqueOwners(address: str) -> None:
    """Get the number of unique owners

    Args:
        address (str): contract address

    Returns:
        None: None
    """
    
    openseaSlug = PostgresConnection().readonly(f"select opensea from slug where address='{address}'")[0][0]
    
    stats = get(openseaBaseEndpointV2, openseaGetCollectionStats(openseaSlug), headers = openseaHeaders).json()
    
    return stats['total']['num_owners']

# async def computeUniqueOwners(address: str) -> int:
#     """Computes the number of unique owners for given address

#     Args:
#         address (str): contract address 

#     Returns:
#         int: how many unique owners there are
#     """

#     response = get(infuraNftApi(address), auth = (os.environ["INFURAKEY"], os.environ["INFURASECRET"])).json()
#     cursor = response['cursor']

#     owners = {i['ownerOf'] for i in response['owners']}
    
#     while cursor != None:
#         response = get(infuraNftApi(address), params={'cursor': cursor}, auth = (os.environ["INFURAKEY"], os.environ["INFURASECRET"])).json()

#         cursor = response['cursor']
#         owners = owners | {i['ownerOf'] for i in response['owners']}
    
#     return len(owners)
        
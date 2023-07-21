"""Gets the floor of a collection."""

from request.getRequest import get

def getCollectionStats(slug):
    endpoint = f"collection/{slug}/stats"
    return get(endpoint)['stats']
    
"""Gets the floor (ETH) of a collection."""
def getFloor(slug):
    stats = getCollectionStats(slug)
    floor = stats['floor_price']
    
    return floor

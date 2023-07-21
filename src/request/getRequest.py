import requests
from keys import openseaKey

baseEndpoint = "https://api.opensea.io/api/v1"

"""Turns parameteres into the format required by the API."""
def generateParams(params):
    result = ""
    if len(params) != 0:
        result += '?'

        p = list(map(lambda k : k[0] + '=' + k[1], params.items()))

        for i in range(0, len(p) - 1):
            result += p[i] + '&'
        result += p[-1]

    return result

"""Does a http GET request.""" 
def get(endpoint, params={}):
    url = f"""{baseEndpoint}/{endpoint}"""

    url += generateParams(params)
    
    print(url)

    headers = {
        "accept":  "application/json",
        "X-API-KEY": f"{openseaKey}"
    }

    return requests.get(url, headers = headers).json()
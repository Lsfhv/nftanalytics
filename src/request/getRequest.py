"""
Handles all HTTP get requests to be made. 
"""

import requests
from keys import openseaKey

baseEndpointV1 = "https://api.opensea.io/api/v1"
baseEndpointV2 = "https://api.opensea.io/v2"

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

"""
Get Request.
v2 = False, v1 api used.
v2 = True, v2 api used.
"""
def get(url, endpoint, params = {}, headers = {}):
    if endpoint != "":
        url = f"""{url}/{endpoint}"""

    url += generateParams(params)
    
    response = requests.get(url, headers = headers)

    while response.status_code != 200:
        print("Response code not 200, trying again ...")
        
        response = requests.get(url, headers = headers)
        

    return response
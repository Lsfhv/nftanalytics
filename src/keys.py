"""
Keys and constants.
"""
import os

# https://opensea.io/
openseaKey = os.environ['OSKEY']

# https://etherscan.io/
etherscanKey = os.environ['ETHERSCANKEY']

# https://www.infura.io/
infuraUrl = os.environ['INFURAURL']

etherscanGetAbi = lambda address, key : f"""https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={key}"""

openseaBaseEndpointV1 = "https://api.opensea.io/api/v1"
openseaBaseEndpointV2 = "https://api.opensea.io/v2"
openseaHeaders = {
    "accept":  "application/json",
    "X-API-KEY": f"{openseaKey}"
}



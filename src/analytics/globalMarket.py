"""
Monitors the global nft market (ERC-721's).
"""

from web3 import Web3
from keys import etherscanKey, infuraUrl, etherscanGetAbi
from request.getRequest import get

blockchain = Web3(Web3.HTTPProvider(infuraUrl))

# def get(address):
#     url = etherscanGetAbi(address, etherscanKey)

#     return requests.get(url)

# response = get(etherscanGetAbi("0x1A92f7381B9F03921564a437210bB9396471050C", etherscanKey), "")
# print(response.json())

class GlobalMarket:
    def __init__(self) -> None:
        pass

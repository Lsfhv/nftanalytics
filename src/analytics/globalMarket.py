"""
Monitors the global nft market (ERC-721's).
"""

from web3 import Web3
from keys import etherscanKey, infuraUrl, etherscanGetAbi, openseaBaseEndpointV1
from request.getRequest import get

lastBlock = None

web3 = Web3(Web3.HTTPProvider(infuraUrl))

def start():

    while True:
        block = web3.eth.get_block('latest')

        if block['number'] != lastBlock:
            for i in block['transactions']:
                if web3.eth.get_transaction_receipt(i)['contractAddress'] != None:

            lastBlock = block['number']







# def get(address):
#     url = etherscanGetAbi(address, etherscanKey)

#     return requests.get(url)

# abi = get(etherscanGetAbi("0x1A92f7381B9F03921564a437210bB9396471050C", etherscanKey), "").json()
# contract = blockchain.eth.contract(address="0x1A92f7381B9F03921564a437210bB9396471050C", abi = abi)

# class GlobalMarket:
#     def __init__(self) -> None:
#         pass

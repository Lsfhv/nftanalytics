"""
Count how many unique holders there are of a collection.
"""
from web3 import Web3
import os
import json

def computeUniqueOwners(address: str):
    w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
    erc721abi = json.load(open('abis/Erc721Abi.json')) 

    contract = w3.eth.contract(address, abi=erc721abi)
    
    totalSupply = contract.functions.totalSupply().call()
    
    owners = set()

    for i in range(0, totalSupply):
        owner = contract.functions.ownerOf(i).call()
        owners.add(owner)

    print(len(owners))

    return (len(owners), totalSupply)

computeUniqueOwners('0x1A92f7381B9F03921564a437210bB9396471050C')


"""
Monitors blockchain events for transfers.
"""
from request.WebsocketConnect import getEvent
import asyncio
from web3 import Web3
import os
from Keys import WETHAddress, BLURPOOLAddress

# Transfer(from, to, tokenid)
transferTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

async def monitorTransfers(address):
    
    w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
    q = asyncio.Queue()
    
    asyncio.create_task(getEvent(address, [transferTopic], q))

    while True:
        message = await asyncio.create_task(q.get())
        txHash = message['params']['result']['transactionHash']

        transaction = w3.eth.get_transaction(txHash)

        ether = transaction["value"]

        print("Ether transfered ... ")
        print(ether)
        events = w3.eth.get_transaction_receipt(txHash)["logs"]

        for event in events:
            if event["topics"][0].hex() == transferTopic:
                
                if event["address"] == address:
                    print("NFT transfer ... ") 
                    print(event["topics"][1].hex(), event["topics"][2].hex())

                if event["address"] == WETHAddress:
                    print("WETH transfer ... ")
                    print(int(event["topics"][3].hex(), 16))

                if event["address"] == BLURPOOLAddress:
                    print("BLUR transfer ... ")
                    print(int(event["topics"][3].hex(), 16))

            



        # transaction = w3.eth.get_transaction(txHash)

        # f = transaction["from"]
        # to = transaction["to"]
        # value = transaction["value"]

        # print(address, f, to, value)



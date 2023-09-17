"""
Monitors blockchain events for transfers.
"""
from request.WebsocketConnect import getEvent
import asyncio
from web3 import Web3
import os

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

        

        f = transaction["from"]
        to = transaction["to"]

        value = transaction["value"]


        print(address, f, to, value)



"""
Monitors blockchain events for transfers.
"""
from request.WebsocketConnect import getEvent
import asyncio

# Transfer(from, to, tokenid)
transferTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

async def monitorTransfers(address):

    q = asyncio.Queue()
    
    asyncio.create_task(getEvent(address, [transferTopic], q))

    while True:

        message = await asyncio.create_task(q.get())

        txHash = message['params']['result']['transactionHash']
        print(txHash)


"""
Monitors blockchain events for transfers.
Update the amount of holders of collection.
"""
from request.WebsocketConnect import getEvent
import asyncio
from web3 import Web3
import os
from Keys import WETHAddress, BLURPOOLAddress
from sql.sqlQGenerator import insertG
from Postgresql import PostgresConnection

# Transfer(from, to, tokenid)
transferTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

async def monitorTransfers(address: str):

    """
    Listens to the blockchain for transfer events.
    Inserts into db how much ether,weth,blurpools where spent on each transfer (The main currencies used for trading erc721s).
    """

    w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
    q = asyncio.Queue()
    
    asyncio.create_task(getEvent(address, [transferTopic], q))

    while True:
        message = await asyncio.create_task(q.get())

        src = hex(int(message['params']['result']['topics'][1], 16))
        dst = hex(int(message['params']['result']['topics'][2], 16))
        tokenId = int(message['params']['result']['topics'][3], 16)
        txHash = message['params']['result']['transactionHash']

        blockNumber = w3.eth.get_transaction(txHash)["blockNumber"]
        timestamp = w3.eth.get_block(blockNumber)["timestamp"]

        sql = insertG("transfers", [txHash, address, src, dst, tokenId, timestamp])
        PostgresConnection().insert(sql)




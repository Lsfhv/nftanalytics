"""
Monitors blockchain events for transfers.
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
        txHash = message['params']['result']['transactionHash']

        transaction = w3.eth.get_transaction(txHash)

        ether = transaction["value"]
        weth = 0
        blur = 0

        src = None
        dst = None
        tokenId = None
        
        blockNumber = w3.eth.get_transaction(txHash)["blockNumber"]
        timestamp = w3.eth.get_block(blockNumber)["timestamp"]
        events = w3.eth.get_transaction_receipt(txHash)["logs"]

        for event in events:
            if event["topics"][0].hex() == transferTopic:
                
                if event["address"].lower() == address:
                    src = event["topics"][1].hex()
                    src = '0x' + src[len(src) - 40 : len(src)]
                    dst = event["topics"][2].hex()
                    dst = '0x' + dst[len(dst) - 40 : len(dst)]
                    tokenId = int(event["topics"][3].hex(), 16)

                if event["address"] == WETHAddress:
                    weth += int(event["data"].hex(), 16)

                if event["address"] == BLURPOOLAddress:
                    blur += int(event["data"].hex(), 16)

        sql = insertG("transfers", [txHash, address, tokenId, src, dst, ether/1e18, weth/1e18, blur/1e18, timestamp])
        PostgresConnection().insert(sql)




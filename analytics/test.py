import asyncio
import json
from websockets import connect 
import os
import asyncio
from web3 import Web3
from Postgresql import PostgresConnection
from Keys import blurMakerPackedTopic, blurPackedTopic, blurTakerPackedTopic, openseaOrderFulfilledTopic
from sql.sqlQGenerator import insertG
import datetime
import sqlite3

class WsConnect:
    def __init__(self) -> None:
        self.ws = None
        self.q = asyncio.Queue(1e9)

        

    async def connect(self) -> None:
        """Connect to ws endpoint
        """     
        self.ws = await connect(f"wss://mainnet.infura.io/ws/v3/{os.environ['INFURAAPIKEY']}")
            
    async def startHandlingMessages(self):
        """Start handling messages

        If subscription response, save the response
        If response to an event, send it to self.q for processing

        """
        while True:
            message = await self.ws.recv()
            message = json.loads(message)
            
       
            await self.q.put(message)

            # print(len(self.subscriptionToAddress))
                
    async def startProcessingMessages(self):
        while True:
            message = await self.q.get()
            print(message)

async def main():
    x = WsConnect()
    await x.connect()
    asyncio.create_task(x.startHandlingMessages())
    asyncio.create_task(x.startProcessingMessages())
    
    await x.ws.send('{"jsonrpc":"2.0","method":"eth_subscribe","params":["logs",{"topics":["0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31"]}],"id":1}')
    await asyncio.sleep(1000000)

asyncio.run(main())
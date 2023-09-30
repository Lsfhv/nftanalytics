"""
Stream data through websockets
"""
import asyncio
import json
from websockets import connect 
import os

def messageBuilder(address, topics):
    data = {"id":1, "method":"eth_subscribe"}
    params = {"address":address, "topics": topics}
    data["params"] = ["logs", params]

    return json.dumps(data)

INFURAAPIKEY = os.environ['INFURAAPIKEY']
async def getEvent(address: str, topics: list[str], q: asyncio.Queue):

    async with connect(f"wss://mainnet.infura.io/ws/v3/{INFURAAPIKEY}") as ws:
        # print(address, topics)
        jsonData = messageBuilder(address, topics)
        
        await ws.send(jsonData)
        subscription_response = await ws.recv()

        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=60000000)
                message = json.loads(message)

                await q.put(message)             
            except Exception as e:
                print("WEBSOCKET ERROR")

                

                ws = await connect(f"wss://mainnet.infura.io/ws/v3/{INFURAAPIKEY}")
                jsonData = messageBuilder(address, topics)
                await ws.send(jsonData)
                subscription_response = await ws.recv()
                
                print("RECONNECTED?")        
                
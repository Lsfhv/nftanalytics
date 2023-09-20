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

        jsonData = messageBuilder(address, topics)

        await ws.send(jsonData)
        subscription_response = await ws.recv()

        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=60)
                message = json.loads(message)
                asyncio.create_task(q.put(message))                
            except:
                pass
                
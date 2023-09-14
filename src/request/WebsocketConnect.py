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
async def getEvent(address, topics):
    async with connect(f"wss://sepolia.infura.io/ws/v3/{INFURAAPIKEY}") as ws:

        jsonData = messageBuilder(address, topics)

        await ws.send(jsonData)
        subscription_response = await ws.recv()

        while True:
            try:
                message = await asyncio.wait_for(ws.recv(), timeout=60)
                print(json.loads(message))
                print()
                pass
            except:
                pass

def main():
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(getEvent("0x4d7020d9E9c44541E4C6Df6DBBa72A9Daf1D4131", ["0x69be8fb95322be2deedcd58a219c0c119e11324a8f2f1419b190f6d36b06f438"]))

main()

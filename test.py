import os
import json
from web3 import Web3
import websockets
import asyncio
import json
def messageBuilder(address, topics):
    data = {"id":1, "method":"eth_subscribe"}
    params = {"address":address, "topics": topics}
    data["params"] = ["logs", params]

    return json.dumps(data)



async def test():

    ws = await websockets.connect(f"wss://mainnet.infura.io/ws/v3/{os.environ['INFURAAPIKEY']}")
    jsonData = messageBuilder('0x60E4d786628Fea6478F785A6d7e704777c86a7c6', ['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'])

    await ws.send(jsonData)
    subscription_response = await ws.recv()

    while True:
        try:
            message = await asyncio.wait_for(ws.recv(), timeout=60000000)
            message = json.loads(message)
            print(message)
        except Exception as e:
            print("WEBSOCKET ERROR")

            ws = connect(f"wss://mainnet.infura.io/ws/v3/{INFURAAPIKEY}")
            # await ws.send(jsonData)
            # subscription_response = await ws.recv()
            # print(e)
            pass


# async def test():
#     async with websockets.connect(f"wss://mainnet.infura.io/ws/v3/{os.environ['INFURAAPIKEY']}") as ws:
#         jsonData = messageBuilder('0x60E4d786628Fea6478F785A6d7e704777c86a7c6', ['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'])
#         print(jsonData)
#         await ws.send(jsonData)
#         subscription_response = await ws.recv()
#         print(subscription_response)
#         while True:
#             try:
#                 message = await asyncio.wait_for(ws.recv(), timeout=60000000)
#                 message = json.loads(message)

#                 # await q.put(message)             
#             except Exception as e:
#                 # print("WEBSOCKET ERROR")

#                 # ws = connect(f"wss://mainnet.infura.io/ws/v3/{INFURAAPIKEY}")
#                 # await ws.send(jsonData)
#                 # subscription_response = await ws.recv()
#                 # print(e)
#                 pass

asyncio.run(test())
# abi ='[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"tokenIdListingIndexTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collectionPriceSide","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"makerFeeRecipientRate","type":"uint256"}],"name":"Execution721MakerFeePacked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"tokenIdListingIndexTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collectionPriceSide","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"takerFeeRecipientRate","type":"uint256"}],"name":"Execution721TakerFeePacked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"tokenIdListingIndexTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collectionPriceSide","type":"uint256"}],"name":"Execution721Packed","type":"event"}]'

# blurMakerPackedTopic = '0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e'
# blurTakerPackedTopic = '0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab'
# blurPackedTopic = '0x1d5e12b51dee5e4d34434576c3fb99714a85f57b0fd546ada4b0bddd736d12b2'

# w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))

# contract = w3.eth.contract(abi=abi)

# receipt = w3.eth.get_transaction_receipt('0xfb41432c1ce845bdff33052c297a9a5cfeaa5d5e01e7e575834ad0e17fd7d7ab')["logs"][3]

# x = contract.events.Execution721TakerFeePacked().process_log(receipt)["args"]




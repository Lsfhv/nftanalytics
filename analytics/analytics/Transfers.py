"""
Monitors blockchain events for transfers.
Update the amount of holders of collection.
"""
# from request.WebsocketConnect import getEvent
import asyncio
from web3 import Web3
import os
from Keys import WETHAddress, BLURPOOLAddress
from sql.sqlQGenerator import insertG
from Postgresql import PostgresConnection
import datetime
from Keys import abi, blurMakerPackedTopic, blurPackedTopic, blurTakerPackedTopic, transferTopic, openseaOrderFulfilledTopic

def getTimestampInEpoch(txHash: str):
    w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
    blockNumber = w3.eth.get_transaction_receipt(txHash)["blockNumber"]

    try:
        timestamp = w3.eth.get_block(blockNumber)["timestamp"]
    except:
        timestamp = 0
    
    return timestamp

async def monitorTransfers(address: str):
    """
    Listens to the blockchain for transfer events.
    """

    w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
    q = asyncio.Queue()
    
    contract = w3.eth.contract(abi=abi)

    asyncio.create_task(getEvent(address, [transferTopic], q))

    while True:
        message = await q.get()

        txHash = message['params']['result']['transactionHash']

        receipt = w3.eth.get_transaction_receipt(txHash)

        src = message['params']['result']['topics'][1]
        src = "0x" + src[len(src) - 40 : ]

        dst = message['params']['result']['topics'][2]
        dst = "0x" + dst[len(dst) - 40 : ]

        token = int(message['params']['result']['topics'][3], 16)
        
        for event in receipt["logs"]:
            eventSignature = event["topics"][0].hex()

            if eventSignature == blurMakerPackedTopic or eventSignature == blurTakerPackedTopic or eventSignature == blurPackedTopic:
                if eventSignature == blurMakerPackedTopic:
                    decoded = contract.events.Execution721MakerFeePacked().process_log(event)["args"]
                elif eventSignature == blurTakerPackedTopic:
                    decoded = contract.events.Execution721TakerFeePacked().process_log(event)["args"]
                else: 
                    decoded = contract.events.Execution721Packed().process_log(event)["args"]

                tokenIdListingIndexTrader = hex(decoded["tokenIdListingIndexTrader"]) 
                collectionPriceSide = hex(decoded["collectionPriceSide"])

                # If blurMakerPackedTopic, then this is the address of the wallet that listed it. The NFT will be transferred from this wallet. i.e trader = src
                # Else, someone sold into bids. Trader = the person whos bid got accepted, the NFT is given to this person. i.e trader = dst
                trader = "0x" + tokenIdListingIndexTrader[len(tokenIdListingIndexTrader) - 40:] 
                tokenId = tokenIdListingIndexTrader[:len(tokenIdListingIndexTrader)-40][2:][:-2]
                tokenId = int(tokenId, 16)
                collection = "0x" + collectionPriceSide[len(collectionPriceSide)-40:]

                if eventSignature == blurMakerPackedTopic:
                    price = collectionPriceSide[:len(collectionPriceSide)-40][2:]
                else:
                    price = collectionPriceSide[:len(collectionPriceSide)-40][2:][1:]
                price = int(price, 16)

                timestamp = getTimestampInEpoch(txHash)
                if (eventSignature == blurMakerPackedTopic and src == trader and collection == address.lower() and token == tokenId) or ((eventSignature == blurTakerPackedTopic or eventSignature == blurPackedTopic) and dst == trader and collection == address.lower() and token == tokenId):
                    sql = insertG("trades", [address, src, dst, tokenId, str(price), txHash, "blur", str(datetime.datetime.fromtimestamp(timestamp))])  
                    PostgresConnection().insert(sql)
            elif eventSignature == openseaOrderFulfilledTopic:
                decoded = contract.events.OrderFulfilled().process_log(event)["args"]

                offerer = decoded['offerer']
                recipient = decoded['recipient']
                
                if src == offerer.lower() and dst == recipient.lower() and token == decoded['offer'][0]['identifier']:  
                    # Listing was sold, make order. 
                    # offerer = the lister, recipeint = the buyer.
                    # print("got here")
                    consideration = decoded['consideration']

                    price = 0
                    for i in consideration:
                        price += i['amount']

                    timestamp = getTimestampInEpoch(txHash)
                    sql = insertG("trades", [address, offerer, recipient, token, str(price), txHash, "opensea", str(datetime.datetime.fromtimestamp(timestamp))])
                    PostgresConnection().insert(sql)
                elif src == recipient.lower() and dst == offerer.lower() and token == decoded['consideration'][0]['identifier']:
                    # Someone sold into bids.
                    # src = the nft holder, dst = the bid poster

                    price = decoded['offer'][0]['amount']

                    timestamp = getTimestampInEpoch(txHash)
                    sql = insertG("trades", [address, recipient, offerer, token, str(price), txHash, "opensea", str(datetime.datetime.fromtimestamp(timestamp))])
                    PostgresConnection().insert(sql)








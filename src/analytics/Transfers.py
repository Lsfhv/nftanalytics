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
import datetime


# Transfer(from, to, tokenid)
transferTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

async def monitorTransfers(address: str):
    """
    Listens to the blockchain for transfer events.
    """
    
    abi ='[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"tokenIdListingIndexTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collectionPriceSide","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"makerFeeRecipientRate","type":"uint256"}],"name":"Execution721MakerFeePacked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"tokenIdListingIndexTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collectionPriceSide","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"takerFeeRecipientRate","type":"uint256"}],"name":"Execution721TakerFeePacked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"tokenIdListingIndexTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collectionPriceSide","type":"uint256"}],"name":"Execution721Packed","type":"event"}]'

    blurMakerPackedTopic = '0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e'
    blurTakerPackedTopic = '0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab'
    blurPackedTopic = '0x1d5e12b51dee5e4d34434576c3fb99714a85f57b0fd546ada4b0bddd736d12b2'
    
    w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
    q = asyncio.Queue()
    
    contract = w3.eth.contract(abi=abi)

    asyncio.create_task(getEvent(address, [transferTopic], q))

    while True:
        message = await q.get()

        txHash = message['params']['result']['transactionHash']

        receipt = w3.eth.get_transaction_receipt(txHash)


        src = message['params']['result']['topics'][1]
        src = "0x" + src[len(src) - 40: ]

        dst = message['params']['result']['topics'][2]
        dst = "0x" + dst[len(dst) - 40: ]

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

                blockNumber = w3.eth.get_transaction_receipt(txHash)["blockNumber"]

                try:
                    timestamp = w3.eth.get_block(blockNumber)["timestamp"]
                except:
                    timestamp = 0

                if (eventSignature == blurMakerPackedTopic and src == trader and collection == address.lower() and token == tokenId) or (eventSignature == blurTakerPackedTopic or eventSignature == blurPackedTopic) and dst == trader and collection == address.lower() and token == tokenId:
                    sql = insertG("trades", [address, src, dst, tokenId, str(price), txHash, "blur", str(datetime.datetime.fromtimestamp(timestamp))])  
                    PostgresConnection().insert(sql)

                

            # if event["topics"][0].hex() == blurMakerPackedTopic:
            #     # Someone bought a listing.
            #     decoded = contract.events.Execution721MakerFeePacked().process_log(event)["args"]

            #     tokenIdListingIndexTrader = hex(decoded["tokenIdListingIndexTrader"]) 
            #     collectionPriceSide = hex(decoded["collectionPriceSide"])

            #     # Decode the inputs to tokenIdListingIndexTrader
            #     trader = "0x" + tokenIdListingIndexTrader[len(tokenIdListingIndexTrader) - 40:] # The address that listed it. The token is transfered from this address.
            #     tokenId = tokenIdListingIndexTrader[:len(tokenIdListingIndexTrader)-40][2:][:-2]
            #     tokenId = int(tokenId, 16)
            #     # Decode the inupts to collectionPriceSide
            #     collection = "0x" + collectionPriceSide[len(collectionPriceSide)-40:]
            #     price = collectionPriceSide[:len(collectionPriceSide)-40][2:]
            #     price = int(price, 16)

            #     if src == trader and collection == address.lower() and token == tokenId:

            #         blockNumber = w3.eth.get_transaction_receipt(txHash)["blockNumber"]
            #         timestamp = w3.eth.get_block(blockNumber)["timestamp"]

            #         sql = insertG("trades", [address, src, dst, tokenId, str(price), txHash, "blur", str(datetime.datetime.fromtimestamp(timestamp))])
            #         PostgresConnection().insert(sql)

            #     # Trader -> Maker, listing fullfilled.

            # if event["topics"][0].hex() == blurTakerPackedTopic:
            #     # Someone sold into bids.
            #     decoded = contract.events.Execution721TakerFeePacked().process_log(event)["args"]

            #     tokenIdListingIndexTrader = hex(decoded["tokenIdListingIndexTrader"])
            #     collectionPriceSide = hex(decoded["collectionPriceSide"])

            #     # Decode the inputs to tokenIdListingIndexTrader
            #     trader = "0x" + tokenIdListingIndexTrader[len(tokenIdListingIndexTrader) - 40:] # The address that had the bid offered. The nft will be transfered to this address.
            #     tokenId = tokenIdListingIndexTrader[:len(tokenIdListingIndexTrader)-40][2:][:-2]
            #     tokenId = int(tokenId, 16)
            #     # Decode inputs to collectionPriceSide
            #     collection = "0x" + collectionPriceSide[len(collectionPriceSide)-40:]
            #     price = collectionPriceSide[:len(collectionPriceSide)-40][2:][1:]
            #     price = int(price, 16)


            #     # print("Taker, ", src, dst, trader, collection, address, price)


            #     if dst == trader and collection == address.lower() and token == tokenId:
                   
            #         blockNumber = w3.eth.get_transaction_receipt(txHash)["blockNumber"]
            #         timestamp = w3.eth.get_block(blockNumber)["timestamp"]
            #         # print(address, src, dst, tokenId, str(price), txHash, "blur",str(datetime.datetime.fromtimestamp(timestamp)) )
            #         sql = insertG("trades", [address, src, dst, tokenId, str(price), txHash, "blur", str(datetime.datetime.fromtimestamp(timestamp))])
            #         PostgresConnection().insert(sql)

            # if event["topics"][0].hex() == blurPackedTopic:
            #     # Same as a taker.
            #     decoded = contract.events.Execution721Packed().process_log(event)["args"]

            #     tokenIdListingIndexTrader = hex(decoded["tokenIdListingIndexTrader"])
            #     collectionPriceSide = hex(decoded["collectionPriceSide"])

            #     trader = "0x" + tokenIdListingIndexTrader[len(tokenIdListingIndexTrader) - 40:]
            #     tokenId = tokenIdListingIndexTrader[:len(tokenIdListingIndexTrader)-40][2:][:-2]
            #     tokenId = int(tokenId, 16)

            #     collection = "0x" + collectionPriceSide[len(collectionPriceSide)-40:]
            #     price = collectionPriceSide[:len(collectionPriceSide)-40][2:][1:]
            #     price = int(price, 16)

            #     if dst == trader and collection == address.lower() and token == tokenId:
                    
            #         blockNumber = w3.eth.get_transaction_receipt(txHash)["blockNumber"]
            #         timestamp = w3.eth.get_block(blockNumber)["timestamp"]

            #         sql = insertG("trades", [address, src, dst, tokenId, str(price), txHash, "blur", str(datetime.datetime.fromtimestamp(timestamp))])
            #         PostgresConnection().insert(sql)



        # txHash = message['params']['result']['transactionHash']

        # try:
        #     blockNumber = w3.eth.get_transaction(txHash)["blockNumber"]
        #     timestamp = w3.eth.get_block(blockNumber)["timestamp"]
        # except:
        #     timestamp = 0

        # sql = insertG("transfers", [txHash, address, src, dst, tokenId, timestamp])
        # PostgresConnection().insert(sql)




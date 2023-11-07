"""
Handle transfers.
"""
import asyncio
import json
from websockets import connect 
import os
import asyncio
from web3 import Web3
from Postgresql import PostgresConnection
from Keys import blurMakerPackedTopic, blurPackedTopic, blurTakerPackedTopic, openseaOrderFulfilledTopic, WETHAddress, ETHAddress, openseaFeeAddress
from sql.sqlQGenerator import insertG
import datetime
import sqlite3

class WsConnect:
    def __init__(self, db) -> None:
        self.isConnected = False
        self.ws = None

        self.db = db

        self.subscriptions = []
        self.subscriptionToAddress = {}

        self.q = asyncio.Queue(1e9)

        self.w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
        f =open('abis/CustomTradesAbi.json')
        self.customTradesAbi = json.load(f)
        f.close()
        self.contract = self.w3.eth.contract(abi= self.customTradesAbi)


        

    async def connect(self) -> None:
        """Connect to ws endpoint
        """     
        self.ws = await connect(f"wss://mainnet.infura.io/ws/v3/{os.environ['INFURAAPIKEY']}")
        
        self.isConnected = True
    
    async def startHandlingMessages(self):
        """Start handling messages

        If subscription response, save the response
        If response to an event, send it to self.q for processing

        """
        while True:
            if self.ws == None or not self.isConnected:
                return 

            message = await self.ws.recv()
            message = json.loads(message)
            
            if 'id' in message and 'result' in message:
                # handle response to a new subscription
                self.subscriptionToAddress[message['result']] = message['id']
            else:
                await self.q.put(message)

            # print(len(self.subscriptionToAddress))

    async def sendMessage(self, address: str, topics: list[str]):
        """Send a message to ws
        
        Args:
            address (str): contract address
            topics (list[str]): topic list to subscribe to 
        """
        if self.ws == None:
            return
        
        message = self.messageBuilder(address, address, topics)

        await self.ws.send(message)

    def messageBuilder(self, id: str, address: str, topics: list[str]) -> dict:
        """Generate the json message that the websocket expects.

        Args:
            id (str): Id of the message
            address (str): Contract address
            topics (list[str]): List of topics to subscribe to

        Returns:
            dict: Dictionary (json) message
        """
        data = {"id": id, "method":"eth_subscribe"}
        params = {"address":address, "topics": topics}
        data["params"] = ["logs", params]

        return json.dumps(data)
    
    def getTimestampInEpoch(self, txHash: str):
        w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
        blockNumber = w3.eth.get_transaction_receipt(txHash)["blockNumber"]

        try:
            timestamp = w3.eth.get_block(blockNumber)["timestamp"]
        except:
            timestamp = 0
        
        return timestamp
    
    def processBlurTrade(self, event):
        pass        
    
    def processOpenseaTrade(self, event):
        decoded = self.contract.events.OrderFulfilled().process_log(event)['args']
        offer = decoded['offer']
        offerer = decoded['offerer']
        recipient = decoded['recipient']
        ofr = []
        value = 0
        for i in offer:
            if i['itemType'] == 0 or i['itemType'] == 1:
                value += i['amount']
            elif i['itemType'] == 2 or i['itemType'] == 3:
                collectionAddress = i['token']
                tokenId = i['identifier']

                ofr = ofr + [collectionAddress, tokenId]
        ofr = ofr + [value]
        
        consideration = decoded['consideration']

        cdr = []
        value = 0
        for i in consideration:
            if i['itemType'] == 0 or i['itemType'] == 1:
                if (i['recipient'] != openseaFeeAddress):
                    value += i['amount']
            elif i['itemType'] == 2 or i['itemType'] == 3:  
                collectionAddress = i['token']
                tokenId = i['identifier']
                cdr = cdr + [collectionAddress, tokenId]
        cdr = cdr + [value]
        result = {'marketplace': 'opensea'}
        if len(cdr) > len(ofr):
            result['src'] = recipient
            result['dst'] = offerer
            result['token'] = cdr[1]
            result['price'] = ofr[0]
            result['collectionAddress'] = cdr[0]
        else:
            result['src'] = offerer
            result['dst'] = recipient
            result['token'] = ofr[1]
            result['price'] = cdr[0]
            result['collectionAddress'] = ofr[0]

        # print("Offerer: ", offerer)
        # print("Recipient: ", recipient)
        # print("Offer: ", ofr)
        # print("Consideration: ", cdr)
        # print()

        # print(result)
        return result
    
    async def startProcessingMessages(self):
        """
        Start processing messages
        """

        self.db.cursor().execute("create table if not exists trades (address varchar(42), src varchar(42), dst varchar(42), tokenid int, price varchar(100), txhash varchar(100), platform varchar(100), timestamp varchar(100))")

        while True:
            message = await self.q.get()
            txHash = message['params']['result']['transactionHash']
            receipt = self.w3.eth.get_transaction_receipt(txHash)
            for event in receipt['logs']:
                eventSignature = event["topics"][0].hex()
                if eventSignature == openseaOrderFulfilledTopic:
                    result = self.processOpenseaTrade(event)
                    result['txHash'] = txHash
                    timestamp = self.getTimestampInEpoch(txHash)
                    sql = insertG("trades", [result['collectionAddress'], result['src'], result['dst'], result['token'], str(result['price']), result['txHash'], result['marketplace'], str(datetime.datetime.fromtimestamp(timestamp))])
                    self.db.cursor().execute(sql)
                    self.db.commit()

                    print(result)


        # while True:
        #     message = await self.q.get()
        #     # print(self.q.qsize()) 
        #     # print(self.q.qsize())

        #     try:
        #         subscription = message['params']['subscription']
        #         address = self.subscriptionToAddress[subscription]

        #         txHash = message['params']['result']['transactionHash']

        #         print(txHash)
                
        #         receipt = self.w3.eth.get_transaction_receipt(txHash)

        #         src = message['params']['result']['topics'][1]
        #         src = "0x" + src[len(src) - 40 : ]

        #         dst = message['params']['result']['topics'][2]
        #         dst = "0x" + dst[len(dst) - 40 : ]

        #         token = int(message['params']['result']['topics'][3], 16)

        #         print("got something")

                
        #         for event in receipt["logs"]:
        #             eventSignature = event["topics"][0].hex()

        #             if eventSignature == blurMakerPackedTopic or eventSignature == blurTakerPackedTopic or eventSignature == blurPackedTopic:
        #                 if eventSignature == blurMakerPackedTopic:
        #                     decoded = self.contract.events.Execution721MakerFeePacked().process_log(event)["args"]
        #                 elif eventSignature == blurTakerPackedTopic:
        #                     decoded = self.contract.events.Execution721TakerFeePacked().process_log(event)["args"]
        #                 else: 
        #                     decoded = self.contract.events.Execution721Packed().process_log(event)["args"]

        #                 tokenIdListingIndexTrader = hex(decoded["tokenIdListingIndexTrader"]) 
        #                 collectionPriceSide = hex(decoded["collectionPriceSide"])

        #                 # If blurMakerPackedTopic, then this is the address of the wallet that listed it. The NFT will be transferred from this wallet. i.e trader = src
        #                 # Else, someone sold into bids. Trader = the person whos bid got accepted, the NFT is given to this person. i.e trader = dst
        #                 trader = "0x" + tokenIdListingIndexTrader[len(tokenIdListingIndexTrader) - 40:] 
        #                 tokenId = tokenIdListingIndexTrader[:len(tokenIdListingIndexTrader)-40][2:][:-2]
        #                 tokenId = int(tokenId, 16)
        #                 collection = "0x" + collectionPriceSide[len(collectionPriceSide)-40:]

        #                 if eventSignature == blurMakerPackedTopic:
        #                     price = collectionPriceSide[:len(collectionPriceSide)-40][2:]
        #                 else:
        #                     price = collectionPriceSide[:len(collectionPriceSide)-40][2:][1:]
        #                 price = int(price, 16)

        #                 timestamp = self.getTimestampInEpoch(txHash)
        #                 if (eventSignature == blurMakerPackedTopic and src == trader and collection == address.lower() and token == tokenId) or ((eventSignature == blurTakerPackedTopic or eventSignature == blurPackedTopic) and dst == trader and collection == address.lower() and token == tokenId):
        #                     sql = insertG("trades", [address, src, dst, tokenId, str(price), txHash, "blur", str(datetime.datetime.fromtimestamp(timestamp))])  
        #                     # PostgresConnection().insert(sql)
        #                     self.db.cursor().execute(sql)
        #                     self.db.commit()
        #             elif eventSignature == openseaOrderFulfilledTopic:
        #                 decoded = self.contract.events.OrderFulfilled().process_log(event)["args"]

        #                 offerer = decoded['offerer']
        #                 recipient = decoded['recipient']
                        
        #                 if src == offerer.lower() and dst == recipient.lower() and token == decoded['offer'][0]['identifier']:  
        #                     # Listing was sold, make order. 
        #                     # offerer = the lister, recipeint = the buyer.
        #                     # print("got here")
        #                     consideration = decoded['consideration']

        #                     price = 0
        #                     for i in consideration:
        #                         price += i['amount']

        #                     timestamp = self.getTimestampInEpoch(txHash)
        #                     sql = insertG("trades", [address, offerer, recipient, token, str(price), txHash, "opensea", str(datetime.datetime.fromtimestamp(timestamp))])
        #                     # PostgresConnection().insert(sql)
        #                     self.db.cursor().execute(sql)
        #                     self.db.commit()
        #                 elif src == recipient.lower() and dst == offerer.lower() and token == decoded['consideration'][0]['identifier']:
        #                     # Someone sold into bids.
        #                     # src = the nft holder, dst = the bid poster

        #                     price = decoded['offer'][0]['amount']

        #                     timestamp = self.getTimestampInEpoch(txHash)
        #                     sql = insertG("trades", [address, recipient, offerer, token, str(price), txHash, "opensea", str(datetime.datetime.fromtimestamp(timestamp))])
        #                     # PostgresConnection().insert(sql)
        #                     self.db.cursor().execute(sql)
        #                     self.db.commit()
        #     except:
        #         pass

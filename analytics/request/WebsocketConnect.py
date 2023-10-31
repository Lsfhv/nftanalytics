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
from Keys import blurMakerPackedTopic, blurPackedTopic, blurTakerPackedTopic, openseaOrderFulfilledTopic
from sql.sqlQGenerator import insertG
import datetime

class WsConnect:

    def __init__(self) -> None:
        self.isConnected = False
        self.ws = None

        self.subscriptions = []
        self.subscriptionToAddress = {}

        self.q = asyncio.Queue()

        self.w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))

        self.customTradesAbi = json.load(open('analytics/abis/CustomTradesAbi.json'))
        
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
    
    async def startProcessingMessages(self):
        """
        Start processing messages
        
        """

        contract = self.w3.eth.contract(abi= self.customTradesAbi)
        while True:
            message = await self.q.get()

            subscription = message['params']['subscription']
            address = self.subscriptionToAddress[subscription]

            txHash = message['params']['result']['transactionHash']

            print("Got a message! ", address, txHash)
            
            receipt = self.w3.eth.get_transaction_receipt(txHash)

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

                    timestamp = self.getTimestampInEpoch(txHash)
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

                        timestamp = self.getTimestampInEpoch(txHash)
                        sql = insertG("trades", [address, offerer, recipient, token, str(price), txHash, "opensea", str(datetime.datetime.fromtimestamp(timestamp))])
                        PostgresConnection().insert(sql)
                    elif src == recipient.lower() and dst == offerer.lower() and token == decoded['consideration'][0]['identifier']:
                        # Someone sold into bids.
                        # src = the nft holder, dst = the bid poster

                        price = decoded['offer'][0]['amount']

                        timestamp = self.getTimestampInEpoch(txHash)
                        sql = insertG("trades", [address, recipient, offerer, token, str(price), txHash, "opensea", str(datetime.datetime.fromtimestamp(timestamp))])
                        PostgresConnection().insert(sql)

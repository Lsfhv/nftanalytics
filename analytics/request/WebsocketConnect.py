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
from Keys import blurMakerPackedTopic, blurPackedTopic, blurTakerPackedTopic, openseaOrderFulfilledTopic, WETHAddress, ETHAddress, openseaFeeAddress, transferTopic
from sql.sqlQGenerator import insertG
import datetime
import sqlite3
from request.getRequest import get
from Keys import openseaBaseEndpointV1, openseaBaseEndpointV2, openseaHeaders


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

        f = open('abis/Erc721Abi.json')
        self.erc721Abi = json.load(f)
        f.close()

        self.contract = self.w3.eth.contract(abi= self.customTradesAbi)

        self.blurTopics = {blurMakerPackedTopic, blurPackedTopic, blurTakerPackedTopic}
        self.tradeTopics = self.blurTopics | {openseaOrderFulfilledTopic}



    async def doesSlugExist(self, collectionAddress: str):
        """
        Check if collection exists in slug
        """
        # try:
            # retrieveContract = lambda address: f"/asset_contract/{address}"
        retrieveContract = lambda address: f"/chain/ethereum/contract/{address}"
        response = self.db.cursor().execute(f"select * from slug where address = '{collectionAddress}'").fetchall()
        if len(response) == 0:
            openseaSlug =  get(openseaBaseEndpointV2, retrieveContract(collectionAddress), headers=openseaHeaders)
            openseaSlug = openseaSlug.json()['collection']
            contract = self.w3.eth.contract(address= collectionAddress, abi = self.erc721Abi)
            try:
                name = contract.functions.name().call()
            except Exception as e:
                name = ""
                print("how?: ", e)
            self.db.cursor().execute(f"insert into slug values ('{collectionAddress}', '{openseaSlug}', '{openseaSlug}', '{name}')")
            self.db.commit()

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
    
    def processBlurTrade(self, event, tokenToTraders):
        firstTopic = event["topics"][0].hex()

        if firstTopic == blurMakerPackedTopic:
            decoded = self.contract.events.Execution721MakerFeePacked().process_log(event)['args']
        elif firstTopic == blurPackedTopic:
            decoded = self.contract.events.Execution721Packed().process_log(event)['args']
        elif firstTopic == blurTakerPackedTopic:
            decoded = self.contract.events.Execution721TakerFeePacked().process_log(event)['args']
        
        tokenIdListingIndexTrader = hex(decoded["tokenIdListingIndexTrader"]) 
        collectionPriceSide = hex(decoded["collectionPriceSide"])

        collection = Web3.to_checksum_address("0x" + collectionPriceSide[len(collectionPriceSide)-40:])
        price = collectionPriceSide[:len(collectionPriceSide)-40][2:]
        if len(collectionPriceSide) == 65:
            price = collectionPriceSide[:len(collectionPriceSide)-40][2:][8:]

        listingIndexTrader = "0x" + tokenIdListingIndexTrader[len(tokenIdListingIndexTrader) - 40:]
        tokenId = int(tokenIdListingIndexTrader[:len(tokenIdListingIndexTrader)-40][2:][:-2],16)

        return  {'marketplace': 'blur', 
            'collectionAddress': collection,
            'token': tokenId,  
            'price': int(price, 16)/1e18,
            'src': tokenToTraders[tokenId][0],
            'dst': tokenToTraders[tokenId][1]
        }  
    
    def processOpenseaTrade(self, event):
        decoded = self.contract.events.OrderFulfilled().process_log(event)['args']
        offer = decoded['offer']
        offerer = decoded['offerer']
        recipient = decoded['recipient']
        consideration = decoded['consideration']

        def helper(arr):
            value = 0
            result = []
            for i in arr:
                if i['itemType'] == 0 or i['itemType'] == 1:
                    value += i['amount']
                elif i['itemType'] == 2 or i['itemType'] == 3:
                    collectionAddress = i['token']
                    tokenId = i['identifier']
                    result = result + [collectionAddress, tokenId]
            result = result + [value]
            return result

        ofr = helper(offer)
        cdr = helper(consideration)        
        
        result = {'marketplace': 'opensea'}
        try:
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
        except:
            print(offer, consideration)
            print("Error processing opensea trade")

        return result
    
    async def startProcessingMessages(self):
        """
        Start processing messages
        """

        self.db.cursor().execute("create table if not exists trades (address varchar(42), src varchar(42), dst varchar(42), tokenid int, price varchar(100), txhash varchar(100), platform varchar(100), timestamp varchar(100))")
        try:
            while True:
                message = await self.q.get()
                txHash = message['params']['result']['transactionHash']
                receipt = self.w3.eth.get_transaction_receipt(txHash)
                tokenToTraders = {}

                logs = receipt['logs']
                logs.sort(key = lambda x : x['topics'][0].hex() != transferTopic)

                for event in receipt['logs']:
                    firstTopic = event["topics"][0].hex()

                    if firstTopic == transferTopic and len(event['topics']) == 4:
                        decoded = self.contract.events.Transfer().process_log(event)['args']
                        tokenToTraders[decoded['tokenId']] = [decoded['from'], decoded['to']]

                    if firstTopic in self.tradeTopics:
                        if firstTopic == openseaOrderFulfilledTopic:
                            result = self.processOpenseaTrade(event)
                        elif firstTopic in self.blurTopics:
                            result = self.processBlurTrade(event, tokenToTraders)
                        
                        result['txHash'] = txHash
                        timestamp = self.getTimestampInEpoch(txHash)

                        try:
                            await self.doesSlugExist(result['collectionAddress'])
                            sql = insertG("trades", [result['collectionAddress'], result['src'], result['dst'], result['token'], str(result['price']), result['txHash'], result['marketplace'], str(datetime.datetime.fromtimestamp(timestamp))])
                            self.db.cursor().execute(sql)
                            self.db.commit()
                        except:
                            pass
        except Exception as e:
            print(e)

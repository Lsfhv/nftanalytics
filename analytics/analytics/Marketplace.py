import asyncio
import os
from web3 import Web3
from request.getRequest import get
from Keys import openseaBaseEndpointV1, openseaBaseEndpointV2, openseaHeaders
from sql.sqlQGenerator import insertG
from datetime import datetime
import json
from hexbytes import HexBytes
class Marketplace:
    def __init__(self, topics, ws, dbConnection):
        self.topics = topics
        self.websocketHandler = ws
        self.dbConnection = dbConnection
        self.q = asyncio.Queue()
        self.w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
        f =open('abis/CustomTradesAbi.json')
        self.customTradesAbi = json.load(f)
        f.close()

        f = open('abis/Erc721Abi.json')
        self.erc721Abi = json.load(f)
        f.close()

        self.contract = self.w3.eth.contract(abi= self.customTradesAbi)

    async def startAll(self):
        for topic in self.topics:
            await self.start(topic)

    async def start(self, topic):
        data = {"id": topic, "method":"eth_subscribe"}
        params = {"topics": [topic]}
        data["params"] = ["logs", params]

        await self.websocketHandler.sendMessage(data, self.q)

    def getTimestampInEpoch(self, txHash: str):
        blockNumber = self.w3.eth.get_transaction_receipt(txHash)["blockNumber"]
        try:
            timestamp = self.w3.eth.get_block(blockNumber)["timestamp"]
        except:
            timestamp = 0
        return timestamp

    def postTrade(self, trade):
        sql = insertG("trades", [
            trade['collectionAddress'], 
            trade['src'], 
            trade['dst'],   
            trade['token'],
            trade['price'],
            trade['txHash'],
            trade['marketplace'],
            str(datetime.fromtimestamp(trade['timestamp']))
        ])
        self.dbConnection.cursor().execute(sql)
        self.dbConnection.commit()
    
    async def doesSlugExist(self, collectionAddress: str):
        """
        Check if collection exists in slug
        """

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

    def transformMessage(self, message):
        """Transform message from infura eth_subscribe method 
        so it can be processed by python3 web3 library

        Args:
            message (dict): Message from infura eth_subscribe method

        Returns:
            dict: Transformed message
        """
        event = message['params']['result']
        event['logIndex'] = int(event['logIndex'],16)
        event['transactionIndex'] = int(event['transactionIndex'],16)
        event['blockNumber'] = int(event['blockNumber'],16)
        event['address'] = Web3.to_checksum_address(event['address'])
        event['transactionHash'] = HexBytes(event['transactionHash'])
        event['data'] = HexBytes(event['data'])
        event['topics'] = [HexBytes(i) for i in event['topics']]
        event['blockHash'] = HexBytes(event['blockHash'])
        return event
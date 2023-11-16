from analytics.Marketplace import Marketplace
from KeysAndConstants import blurMakerPackedTopic, blurPackedTopic, blurTakerPackedTopic, transferTopic
import asyncio
from web3 import Web3
class Blur(Marketplace):
    def __init__(self, ws, dbConnection):
        self.topics = [
            blurMakerPackedTopic, 
            blurPackedTopic, 
            blurTakerPackedTopic
        ]

        super().__init__(self.topics, ws, dbConnection)
        asyncio.create_task(self.startProcessingTrades())

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

    async def startProcessingTrades(self):
        while True:
            message = await self.q.get()
            txHash = message['params']['result']['transactionHash']
            logs = self.w3.eth.get_transaction_receipt(txHash)['logs']
            tokenToTraders = {}

            transferEvents = [i for i in logs if i['topics'][0].hex() == transferTopic and len(i['topics']) == 4]
            blurEvents = [i for i in logs if i['topics'][0].hex() in self.topics]

            for transferEvent in transferEvents:
                decoded = self.contract.events.Transfer().process_log(transferEvent)['args']
                tokenToTraders[decoded['tokenId']] = [decoded['from'], decoded['to']]

            for blurEvent in blurEvents:
                result = self.processBlurTrade(blurEvent, tokenToTraders)
                result['txHash'] = txHash
                timestamp = super().getTimestampInEpoch(txHash)
                result['timestamp'] = timestamp
                super().postTrade(result)



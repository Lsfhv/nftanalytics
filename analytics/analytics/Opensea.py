from analytics.Marketplace import Marketplace
from KeysAndConstants import openseaOrderFulfilledTopic
import asyncio
from web3 import Web3
from hexbytes import HexBytes
class Opensea(Marketplace):
    def __init__(self, ws, dbConnection):
        self.topics = [openseaOrderFulfilledTopic]
        super().__init__(self.topics, ws, dbConnection )

        asyncio.create_task(self.startProcessingTrades())

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
                result['price'] = str(ofr[0])
                result['collectionAddress'] = cdr[0]
            else:
                result['src'] = offerer
                result['dst'] = recipient
                result['token'] = ofr[1]
                result['price'] = str(cdr[0])
                result['collectionAddress'] = ofr[0]
        except:
            print(offer, consideration)
            print("Error processing opensea trade")

        return result

    async def startProcessingTrades(self):
        while True:
            message = await self.q.get()    
            event = super().transformMessage(message)
            result = self.processOpenseaTrade(event)
            result['txHash'] = message['params']['result']['transactionHash'].hex()
            result['timestamp'] = super().getTimestampInEpoch(result['txHash'])
            super().postTrade(result)

                
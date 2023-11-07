from web3 import Web3
import os
import json
f =open('abis/CustomTradesAbi.json')
customTradesAbi = json.load(f)
f.close()
w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
x = w3.eth.get_transaction_receipt('0x2b379dac801ff4c69b35aaf3cda82b3271e21718781dc53f9d46966724113170')
contract = w3.eth.contract(abi = customTradesAbi)
openseaOrderFulfilledTopic = '0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31'
openseaFeeAddress = '0x0000a26b00c1F0DF003000390027140000fAa719'
for i in x['logs']:
    eventSignature = i["topics"][0].hex()
    if (eventSignature == openseaOrderFulfilledTopic):
        decoded = contract.events.OrderFulfilled().process_log(i)['args']
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

        print("Offerer: ", offerer)
        print("Recipient: ", recipient)
        print("Offer: ", ofr)
        print("Consideration: ", cdr)
        print()

        print(result)

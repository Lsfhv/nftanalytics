from web3 import Web3
import os
import json
f =open('abis/CustomTradesAbi.json')
customTradesAbi = json.load(f)
f.close()

f =open('abis/Erc721Abi.json')
erc721abi = json.load(f)
f.close()

"""

0xb76df6f7f5ecfa4652ec8f49bdb91122b07d75ad26604432a58e524045378d43 maker
0x3ab5459d1bfec6cbbdae74d88e1268d699cfb3eb3137e26e041069ac499122e2 packed
0xc98af7699a483f814550461498d3b2de2ae057109190b6285a5606524c916597 takers
"""



w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
x = w3.eth.get_transaction_receipt('0xc98af7699a483f814550461498d3b2de2ae057109190b6285a5606524c916597')
contract = w3.eth.contract(abi = customTradesAbi)
erc721contract = w3.eth.contract(abi = erc721abi)
openseaOrderFulfilledTopic = '0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31'
openseaFeeAddress = '0x0000a26b00c1F0DF003000390027140000fAa719'
# Execution721MakerFeePacked
blurMakerPackedTopic = '0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e'

# Execution721TakerFeePacked
blurTakerPackedTopic = '0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab'

# Execution721Packed
blurPackedTopic = '0x1d5e12b51dee5e4d34434576c3fb99714a85f57b0fd546ada4b0bddd736d12b2'

# OrderFulfilled
openseaOrderFulfilledTopic = '0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31'
transferTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

blurbidding = '0x0000000000a39bb272e79075ade125fd351887ac'

blurTopics = {blurMakerPackedTopic, blurPackedTopic, blurTakerPackedTopic}

logs = x['logs']

logs.sort(key = lambda x : x['topics'][0].hex() != transferTopic)
# print(list(map(lambda x : x['topics'][0].hex() == transferTopic, logs)))
tokenToTraders = {}
for i in logs:
    eventSignature = i["topics"][0].hex()
    

    if eventSignature == transferTopic and len(i['topics']) == 4:
        # decoded = contract.events.Transfer().process_log(i)['args']
        decoded = contract.events.Transfer().process_log(i)['args']

        tokenToTraders[decoded['tokenId']] = [decoded['from'], decoded['to']]


    if eventSignature in blurTopics:
        # decoded = contract.events.OrderFulfilled().process_log(i)['args']
        if eventSignature == blurMakerPackedTopic:
            decoded = contract.events.Execution721MakerFeePacked().process_log(i)['args']
        elif eventSignature == blurPackedTopic:
            decoded = contract.events.Execution721Packed().process_log(i)['args']
        elif eventSignature == blurTakerPackedTopic:
            decoded = contract.events.Execution721TakerFeePacked().process_log(i)['args']

        tokenIdListingIndexTrader = hex(decoded["tokenIdListingIndexTrader"]) 
        collectionPriceSide = hex(decoded["collectionPriceSide"])

        side = False
        collection = "0x" + collectionPriceSide[len(collectionPriceSide)-40:]
        price = collectionPriceSide[:len(collectionPriceSide)-40][2:]
        if len(collectionPriceSide) == 65:
            price = collectionPriceSide[:len(collectionPriceSide)-40][2:][8:]
            side = True

        collection = Web3.to_checksum_address(collection)
        # print(side)

        listingIndexTrader = "0x" + tokenIdListingIndexTrader[len(tokenIdListingIndexTrader) - 40:]
        tokenId = int(tokenIdListingIndexTrader[:len(tokenIdListingIndexTrader)-40][2:][:-2],16)

        result = {'marketplace': 'blur', 
                'collectionAddress': collection,
                'token': tokenId,  
                'price': int(price, 16)/1e18,
                'src': tokenToTraders[tokenId][0],
                'dst': tokenToTraders[tokenId][1]}  

        print(result)
        




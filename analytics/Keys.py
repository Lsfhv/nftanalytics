"""
Keys and constants.
"""
import os

# https://app.infura.io/dashboard
infuraurl = lambda x : f"https://mainnet.infura.io/v3/{x}"
infuraurlsepolia = lambda x : f"https://sepolia.infura.io/v3/{x}"

# infura nft api
# curl -X 'GET' \
#   -u $INFURAKEY:$INFURASECRET \
#   'https://nft.api.infura.io/networks/1/nfts/0x1A92f7381B9F03921564a437210bB9396471050C/owners' \
#   -H 'accept: application/json'

infuraNftApi = lambda address : f'https://nft.api.infura.io/networks/1/nfts/{address}/owners'

# https://opensea.io/
openseaKey = os.environ['OSKEY']

# https://etherscan.io/
# etherscanKey = os.environ['ETHERSCANKEY']

# https://www.infura.io/
infuraUrl = os.environ['INFURAURL']

# etherscanGetAbi = lambda address, key : f"""https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={key}"""

openseaBaseEndpointV1 = "https://api.opensea.io/api/v1"
openseaBaseEndpointV2 = "https://api.opensea.io/v2"
openseaHeaders = {
    "accept":  "application/json",
    "X-API-KEY": f"{openseaKey}"
}

# collection stats endpoint
openseaGetCollectionStats = lambda collection_slug : f"collections/{collection_slug}/stats"

WETHAddress = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
BLURPOOLAddress = '0x0000000000A39bb272e79075ade125fd351887Ac'

# huge abi containing seaport + all the method and functions we need.
abi = ''

# Transfer(from, to, tokenid) as per ERC721 standard
transferTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

# Execution721MakerFeePacked
blurMakerPackedTopic = '0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e'

# Execution721TakerFeePacked
blurTakerPackedTopic = '0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab'

# Execution721Packed
blurPackedTopic = '0x1d5e12b51dee5e4d34434576c3fb99714a85f57b0fd546ada4b0bddd736d12b2'

# OrderFulfilled
openseaOrderFulfilledTopic = '0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31'


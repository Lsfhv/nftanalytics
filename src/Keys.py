"""
Keys and constants.
"""
import os

# https://app.infura.io/dashboard
infuraurl = lambda x : f"https://mainnet.infura.io/v3/{x}"
infuraurlsepolia = lambda x : f"https://sepolia.infura.io/v3/{x}"

# https://opensea.io/
openseaKey = os.environ['OSKEY']

# https://etherscan.io/
etherscanKey = os.environ['ETHERSCANKEY']

# https://www.infura.io/
infuraUrl = os.environ['INFURAURL']

etherscanGetAbi = lambda address, key : f"""https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={key}"""

openseaBaseEndpointV1 = "https://api.opensea.io/api/v1"
openseaBaseEndpointV2 = "https://api.opensea.io/v2"
openseaHeaders = {
    "accept":  "application/json",
    "X-API-KEY": f"{openseaKey}"
}

WETHAddress = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
BLURPOOLAddress = '0x0000000000A39bb272e79075ade125fd351887Ac'

# huge abi containing seaport + all the method and functions we need.
abi = '[{"inputs":[{"internalType":"address","name":"conduitController","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"BadContractSignature","type":"error"},{"inputs":[],"name":"BadFraction","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"BadReturnValueFromERC20OnTransfer","type":"error"},{"inputs":[{"internalType":"uint8","name":"v","type":"uint8"}],"name":"BadSignatureV","type":"error"},{"inputs":[],"name":"CannotCancelOrder","type":"error"},{"inputs":[],"name":"ConsiderationCriteriaResolverOutOfRange","type":"error"},{"inputs":[],"name":"ConsiderationLengthNotEqualToTotalOriginal","type":"error"},{"inputs":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"considerationIndex","type":"uint256"},{"internalType":"uint256","name":"shortfallAmount","type":"uint256"}],"name":"ConsiderationNotMet","type":"error"},{"inputs":[],"name":"CriteriaNotEnabledForItem","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256[]","name":"identifiers","type":"uint256[]"},{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"name":"ERC1155BatchTransferGenericFailure","type":"error"},{"inputs":[],"name":"InexactFraction","type":"error"},{"inputs":[],"name":"InsufficientNativeTokensSupplied","type":"error"},{"inputs":[],"name":"Invalid1155BatchTransferEncoding","type":"error"},{"inputs":[],"name":"InvalidBasicOrderParameterEncoding","type":"error"},{"inputs":[{"internalType":"address","name":"conduit","type":"address"}],"name":"InvalidCallToConduit","type":"error"},{"inputs":[{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"address","name":"conduit","type":"address"}],"name":"InvalidConduit","type":"error"},{"inputs":[{"internalType":"bytes32","name":"orderHash","type":"bytes32"}],"name":"InvalidContractOrder","type":"error"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"InvalidERC721TransferAmount","type":"error"},{"inputs":[],"name":"InvalidFulfillmentComponentData","type":"error"},{"inputs":[{"internalType":"uint256","name":"value","type":"uint256"}],"name":"InvalidMsgValue","type":"error"},{"inputs":[],"name":"InvalidNativeOfferItem","type":"error"},{"inputs":[],"name":"InvalidProof","type":"error"},{"inputs":[{"internalType":"bytes32","name":"orderHash","type":"bytes32"}],"name":"InvalidRestrictedOrder","type":"error"},{"inputs":[],"name":"InvalidSignature","type":"error"},{"inputs":[],"name":"InvalidSigner","type":"error"},{"inputs":[{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"}],"name":"InvalidTime","type":"error"},{"inputs":[{"internalType":"uint256","name":"fulfillmentIndex","type":"uint256"}],"name":"MismatchedFulfillmentOfferAndConsiderationComponents","type":"error"},{"inputs":[{"internalType":"enum Side","name":"side","type":"uint8"}],"name":"MissingFulfillmentComponentOnAggregation","type":"error"},{"inputs":[],"name":"MissingItemAmount","type":"error"},{"inputs":[],"name":"MissingOriginalConsiderationItems","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"NativeTokenTransferGenericFailure","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"NoContract","type":"error"},{"inputs":[],"name":"NoReentrantCalls","type":"error"},{"inputs":[],"name":"NoSpecifiedOrdersAvailable","type":"error"},{"inputs":[],"name":"OfferAndConsiderationRequiredOnFulfillment","type":"error"},{"inputs":[],"name":"OfferCriteriaResolverOutOfRange","type":"error"},{"inputs":[{"internalType":"bytes32","name":"orderHash","type":"bytes32"}],"name":"OrderAlreadyFilled","type":"error"},{"inputs":[{"internalType":"enum Side","name":"side","type":"uint8"}],"name":"OrderCriteriaResolverOutOfRange","type":"error"},{"inputs":[{"internalType":"bytes32","name":"orderHash","type":"bytes32"}],"name":"OrderIsCancelled","type":"error"},{"inputs":[{"internalType":"bytes32","name":"orderHash","type":"bytes32"}],"name":"OrderPartiallyFilled","type":"error"},{"inputs":[],"name":"PartialFillsNotEnabledForOrder","type":"error"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"TokenTransferGenericFailure","type":"error"},{"inputs":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"considerationIndex","type":"uint256"}],"name":"UnresolvedConsiderationCriteria","type":"error"},{"inputs":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"offerIndex","type":"uint256"}],"name":"UnresolvedOfferCriteria","type":"error"},{"inputs":[],"name":"UnusedItemParameters","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newCounter","type":"uint256"},{"indexed":true,"internalType":"address","name":"offerer","type":"address"}],"name":"CounterIncremented","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":true,"internalType":"address","name":"offerer","type":"address"},{"indexed":true,"internalType":"address","name":"zone","type":"address"}],"name":"OrderCancelled","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":true,"internalType":"address","name":"offerer","type":"address"},{"indexed":true,"internalType":"address","name":"zone","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"indexed":false,"internalType":"struct SpentItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"indexed":false,"internalType":"struct ReceivedItem[]","name":"consideration","type":"tuple[]"}],"name":"OrderFulfilled","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalConsiderationItems","type":"uint256"}],"indexed":false,"internalType":"struct OrderParameters","name":"orderParameters","type":"tuple"}],"name":"OrderValidated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32[]","name":"orderHashes","type":"bytes32[]"}],"name":"OrdersMatched","type":"event"},{"inputs":[{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"counter","type":"uint256"}],"internalType":"struct OrderComponents[]","name":"orders","type":"tuple[]"}],"name":"cancel","outputs":[{"internalType":"bool","name":"cancelled","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalConsiderationItems","type":"uint256"}],"internalType":"struct OrderParameters","name":"parameters","type":"tuple"},{"internalType":"uint120","name":"numerator","type":"uint120"},{"internalType":"uint120","name":"denominator","type":"uint120"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"internalType":"struct AdvancedOrder","name":"","type":"tuple"},{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"enum Side","name":"side","type":"uint8"},{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"bytes32[]","name":"criteriaProof","type":"bytes32[]"}],"internalType":"struct CriteriaResolver[]","name":"","type":"tuple[]"},{"internalType":"bytes32","name":"fulfillerConduitKey","type":"bytes32"},{"internalType":"address","name":"recipient","type":"address"}],"name":"fulfillAdvancedOrder","outputs":[{"internalType":"bool","name":"fulfilled","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalConsiderationItems","type":"uint256"}],"internalType":"struct OrderParameters","name":"parameters","type":"tuple"},{"internalType":"uint120","name":"numerator","type":"uint120"},{"internalType":"uint120","name":"denominator","type":"uint120"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"internalType":"struct AdvancedOrder[]","name":"","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"enum Side","name":"side","type":"uint8"},{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"bytes32[]","name":"criteriaProof","type":"bytes32[]"}],"internalType":"struct CriteriaResolver[]","name":"","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"itemIndex","type":"uint256"}],"internalType":"struct FulfillmentComponent[][]","name":"","type":"tuple[][]"},{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"itemIndex","type":"uint256"}],"internalType":"struct FulfillmentComponent[][]","name":"","type":"tuple[][]"},{"internalType":"bytes32","name":"fulfillerConduitKey","type":"bytes32"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"maximumFulfilled","type":"uint256"}],"name":"fulfillAvailableAdvancedOrders","outputs":[{"internalType":"bool[]","name":"","type":"bool[]"},{"components":[{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ReceivedItem","name":"item","type":"tuple"},{"internalType":"address","name":"offerer","type":"address"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"}],"internalType":"struct Execution[]","name":"","type":"tuple[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalConsiderationItems","type":"uint256"}],"internalType":"struct OrderParameters","name":"parameters","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct Order[]","name":"","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"itemIndex","type":"uint256"}],"internalType":"struct FulfillmentComponent[][]","name":"","type":"tuple[][]"},{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"itemIndex","type":"uint256"}],"internalType":"struct FulfillmentComponent[][]","name":"","type":"tuple[][]"},{"internalType":"bytes32","name":"fulfillerConduitKey","type":"bytes32"},{"internalType":"uint256","name":"maximumFulfilled","type":"uint256"}],"name":"fulfillAvailableOrders","outputs":[{"internalType":"bool[]","name":"","type":"bool[]"},{"components":[{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ReceivedItem","name":"item","type":"tuple"},{"internalType":"address","name":"offerer","type":"address"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"}],"internalType":"struct Execution[]","name":"","type":"tuple[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"considerationToken","type":"address"},{"internalType":"uint256","name":"considerationIdentifier","type":"uint256"},{"internalType":"uint256","name":"considerationAmount","type":"uint256"},{"internalType":"address payable","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"internalType":"address","name":"offerToken","type":"address"},{"internalType":"uint256","name":"offerIdentifier","type":"uint256"},{"internalType":"uint256","name":"offerAmount","type":"uint256"},{"internalType":"enum BasicOrderType","name":"basicOrderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"offererConduitKey","type":"bytes32"},{"internalType":"bytes32","name":"fulfillerConduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalAdditionalRecipients","type":"uint256"},{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct AdditionalRecipient[]","name":"additionalRecipients","type":"tuple[]"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct BasicOrderParameters","name":"parameters","type":"tuple"}],"name":"fulfillBasicOrder","outputs":[{"internalType":"bool","name":"fulfilled","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"considerationToken","type":"address"},{"internalType":"uint256","name":"considerationIdentifier","type":"uint256"},{"internalType":"uint256","name":"considerationAmount","type":"uint256"},{"internalType":"address payable","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"internalType":"address","name":"offerToken","type":"address"},{"internalType":"uint256","name":"offerIdentifier","type":"uint256"},{"internalType":"uint256","name":"offerAmount","type":"uint256"},{"internalType":"enum BasicOrderType","name":"basicOrderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"offererConduitKey","type":"bytes32"},{"internalType":"bytes32","name":"fulfillerConduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalAdditionalRecipients","type":"uint256"},{"components":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct AdditionalRecipient[]","name":"additionalRecipients","type":"tuple[]"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct BasicOrderParameters","name":"parameters","type":"tuple"}],"name":"fulfillBasicOrder_efficient_6GL6yc","outputs":[{"internalType":"bool","name":"fulfilled","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalConsiderationItems","type":"uint256"}],"internalType":"struct OrderParameters","name":"parameters","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct Order","name":"","type":"tuple"},{"internalType":"bytes32","name":"fulfillerConduitKey","type":"bytes32"}],"name":"fulfillOrder","outputs":[{"internalType":"bool","name":"fulfilled","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"contractOfferer","type":"address"}],"name":"getContractOffererNonce","outputs":[{"internalType":"uint256","name":"nonce","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"offerer","type":"address"}],"name":"getCounter","outputs":[{"internalType":"uint256","name":"counter","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"counter","type":"uint256"}],"internalType":"struct OrderComponents","name":"","type":"tuple"}],"name":"getOrderHash","outputs":[{"internalType":"bytes32","name":"orderHash","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"orderHash","type":"bytes32"}],"name":"getOrderStatus","outputs":[{"internalType":"bool","name":"isValidated","type":"bool"},{"internalType":"bool","name":"isCancelled","type":"bool"},{"internalType":"uint256","name":"totalFilled","type":"uint256"},{"internalType":"uint256","name":"totalSize","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"incrementCounter","outputs":[{"internalType":"uint256","name":"newCounter","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"information","outputs":[{"internalType":"string","name":"version","type":"string"},{"internalType":"bytes32","name":"domainSeparator","type":"bytes32"},{"internalType":"address","name":"conduitController","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalConsiderationItems","type":"uint256"}],"internalType":"struct OrderParameters","name":"parameters","type":"tuple"},{"internalType":"uint120","name":"numerator","type":"uint120"},{"internalType":"uint120","name":"denominator","type":"uint120"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"internalType":"struct AdvancedOrder[]","name":"","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"enum Side","name":"side","type":"uint8"},{"internalType":"uint256","name":"index","type":"uint256"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"bytes32[]","name":"criteriaProof","type":"bytes32[]"}],"internalType":"struct CriteriaResolver[]","name":"","type":"tuple[]"},{"components":[{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"itemIndex","type":"uint256"}],"internalType":"struct FulfillmentComponent[]","name":"offerComponents","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"itemIndex","type":"uint256"}],"internalType":"struct FulfillmentComponent[]","name":"considerationComponents","type":"tuple[]"}],"internalType":"struct Fulfillment[]","name":"","type":"tuple[]"},{"internalType":"address","name":"recipient","type":"address"}],"name":"matchAdvancedOrders","outputs":[{"components":[{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ReceivedItem","name":"item","type":"tuple"},{"internalType":"address","name":"offerer","type":"address"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"}],"internalType":"struct Execution[]","name":"","type":"tuple[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalConsiderationItems","type":"uint256"}],"internalType":"struct OrderParameters","name":"parameters","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct Order[]","name":"","type":"tuple[]"},{"components":[{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"itemIndex","type":"uint256"}],"internalType":"struct FulfillmentComponent[]","name":"offerComponents","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"orderIndex","type":"uint256"},{"internalType":"uint256","name":"itemIndex","type":"uint256"}],"internalType":"struct FulfillmentComponent[]","name":"considerationComponents","type":"tuple[]"}],"internalType":"struct Fulfillment[]","name":"","type":"tuple[]"}],"name":"matchOrders","outputs":[{"components":[{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ReceivedItem","name":"item","type":"tuple"},{"internalType":"address","name":"offerer","type":"address"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"}],"internalType":"struct Execution[]","name":"","type":"tuple[]"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"components":[{"internalType":"address","name":"offerer","type":"address"},{"internalType":"address","name":"zone","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"}],"internalType":"struct OfferItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifierOrCriteria","type":"uint256"},{"internalType":"uint256","name":"startAmount","type":"uint256"},{"internalType":"uint256","name":"endAmount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"internalType":"struct ConsiderationItem[]","name":"consideration","type":"tuple[]"},{"internalType":"enum OrderType","name":"orderType","type":"uint8"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"bytes32","name":"zoneHash","type":"bytes32"},{"internalType":"uint256","name":"salt","type":"uint256"},{"internalType":"bytes32","name":"conduitKey","type":"bytes32"},{"internalType":"uint256","name":"totalOriginalConsiderationItems","type":"uint256"}],"internalType":"struct OrderParameters","name":"parameters","type":"tuple"},{"internalType":"bytes","name":"signature","type":"bytes"}],"internalType":"struct Order[]","name":"","type":"tuple[]"}],"name":"validate","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}, {"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"tokenIdListingIndexTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collectionPriceSide","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"makerFeeRecipientRate","type":"uint256"}],"name":"Execution721MakerFeePacked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"tokenIdListingIndexTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collectionPriceSide","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"takerFeeRecipientRate","type":"uint256"}],"name":"Execution721TakerFeePacked","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"tokenIdListingIndexTrader","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"collectionPriceSide","type":"uint256"}],"name":"Execution721Packed","type":"event"}]'

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


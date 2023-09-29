const Web3 = require('web3');


// const w3 = new Web3("https://mainnet.infura.io/v3/b733902d9de349448dd8a88304ae04cb");

let abi = '{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":true,"internalType":"address","name":"offerer","type":"address"},{"indexed":true,"internalType":"address","name":"zone","type":"address"},{"indexed":false,"internalType":"address","name":"recipient","type":"address"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"indexed":false,"internalType":"struct SpentItem[]","name":"offer","type":"tuple[]"},{"components":[{"internalType":"enum ItemType","name":"itemType","type":"uint8"},{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"identifier","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address payable","name":"recipient","type":"address"}],"indexed":false,"internalType":"struct ReceivedItem[]","name":"consideration","type":"tuple[]"}],"name":"OrderFulfilled","type":"event"}'
abi = JSON.parse(abi).inputs
// console.log(abi);

const data = '0x148bc42be2543974becfbe1b8ab60b6de05202f578a25424f008a000313a08020000000000000000000000004e012d25472225f3385baa43ed64dfec5885c51d00000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000020000000000000000000000001a92f7381b9f03921564a437210bb9396471050c000000000000000000000000000000000000000000000000000000000000127200000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000079838f9bd5520000000000000000000000000006d7b2c59d98f2e007314d57cefff8ffac8f38dbf0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009c51c4521e0000000000000000000000000000000a26b00c1f0df003000390027140000faa719'
const topics = ['0x0000000000000000000000006d7b2c59d98f2e007314d57cefff8ffac8f38dbf', '0x000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00']

// w3.eth.abi.decode
const x = Web3.eth.abi.decodeLog(abi, data, topics)
console.log(x)
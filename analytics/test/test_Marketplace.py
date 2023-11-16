import unittest
from analytics.Marketplace import Marketplace
from hexbytes import HexBytes
from web3 import Web3
import sqlite3
from KeysAndConstants import SLUGTABLE, TRADESTABLE
class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.dbConnection = sqlite3.connect(':memory:')
        self.marketplace = Marketplace(None, None, self.dbConnection)
        self.sampleMessage = {
            "jsonrpc": "2.0",
            "method": "eth_subscription",
            "params": {
                "subscription": "0x10ff11e3e10a217708f3397e1442af211e08a6ec908e",
                "result": {
                "removed": False,
                "logIndex": "0x224",
                "transactionIndex": "0xba",
                "transactionHash": "0xbba60c944d5ddc040afc621c4df8aa0348977c4916da50d297bb2dd0110057a9",
                "blockHash": "0x4df72b06865e13a4836c5b7789c99afa93eb243831544311d2678d1493de3590",
                "blockNumber": "0x11b967f",
                "address": "0x00000000000000adc04c56bf30ac9d3c0aaf14dc",
                "data": "0x6d635d7397c85410b2cc8b723d73eee6cbdc8763fce79cff346a3e0792eaf9eb00000000000000000000000090c1d31feadd57c7c74ef1b77d1b8cc4a997139a000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000001200000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000200000000000000000000000060e4d786628fea6478f785a6d7e704777c86a7c60000000000000000000000000000000000000000000000000000000000005d780000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000052b659e5b5912000000000000000000000000000eb0abe3e9f38fc74ed900f118744275af3a99618000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006a675dc705e0000000000000000000000000000000a26b00c1f0df003000390027140000faa719",
                "topics": [
                    "0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31",
                    "0x000000000000000000000000eb0abe3e9f38fc74ed900f118744275af3a99618",
                    "0x000000000000000000000000004c00500000ad104d7dbd00e3ae0a5c00560c00"
                ]}}}
        self.eventKeys = self.sampleMessage['params']['result'].keys()
        self.integerKeys = ['logIndex', 'transactionIndex', 'blockNumber']
        self.hexKeys = ['transactionHash', 'blockHash', 'data']
        self.coolcatsAddress = '0x1a92f7381b9f03921564a437210bb9396471050c'
        self.sampleTrade = {'marketplace': 'opensea',
                            'src': '0x6a51C6d4Eaa88A5F05A920CF92a1C976250711B4',
                            'dst': '0xDD328BeBf67F4365b372d3dc0e93d070F1873Ddc',
                            'token': 10829, 
                            'price': 90000000000000000,
                            'collectionAddress': '0x76BE3b62873462d2142405439777e971754E8E77',
                            'txHash': '0x12e9edee00e05883c3bf7acbf67406c464e044508aa391f5b41c1fba4f8d983d',
                            'timestamp': 1700164247}


    def test_transformMessage(self):
        event = self.marketplace.transformMessage(self.sampleMessage)
        
        # The event has 9 keys
        self.assertTrue(len(event) == 9)

        # Every key in the event is in the sample message
        for i in self.eventKeys:
            self.assertTrue(i in event.keys())

        # Every integer key is of type int
        for i in self.integerKeys:
            self.assertTrue(isinstance(event[i], int))
        
        # Every hex key is of type hexbytes
        for i in self.hexKeys:
            self.assertTrue(isinstance(event[i], HexBytes))

        # Address is of type string and is checksummed
        self.assertTrue(isinstance(event['address'], str))
        self.assertTrue(event['address'] == Web3.to_checksum_address(event['address']))

        # Every topic is of type hexbytes
        self.assertTrue(isinstance(event['topics'], list))
        for i in event['topics']:
            self.assertTrue(isinstance(i, HexBytes))

    def test_doesSlugExist(self):
        # Verify that table does not exist
        self.assertRaises(sqlite3.OperationalError, self.dbConnection.cursor().execute, "select * from slug")

        self.marketplace.doesSlugExist(self.coolcatsAddress)    
        
        # Check if table was created with 1 row
        self.assertTrue(len(self.dbConnection.cursor().execute("select * from slug").fetchall()) == 1)

        # Check if the row has the correct values
        self.assertTrue(self.dbConnection.cursor().execute(f"select * from {SLUGTABLE}").fetchall()[0][0] == Web3.to_checksum_address(self.coolcatsAddress))
        self.assertTrue(self.dbConnection.cursor().execute("select * from slug").fetchall()[0][1] == 'cool-cats-nft')
        self.assertTrue(self.dbConnection.cursor().execute("select * from slug").fetchall()[0][2] == 'cool-cats-nft')
        self.assertTrue(self.dbConnection.cursor().execute("select * from slug").fetchall()[0][3] == 'Cool Cats')

        # Check if columns are named correctly
        self.assertTrue(self.dbConnection.cursor().execute("select address from slug").fetchall()[0][0] == Web3.to_checksum_address(self.coolcatsAddress))
        self.assertTrue(self.dbConnection.cursor().execute("select openseaSlug from slug").fetchall()[0][0] == 'cool-cats-nft')
        self.assertTrue(self.dbConnection.cursor().execute("select blurSlug from slug").fetchall()[0][0] == 'cool-cats-nft')
        self.assertTrue(self.dbConnection.cursor().execute("select name from slug").fetchall()[0][0] == 'Cool Cats')

    def test_postTrade(self):
        # Verify that table does not exist
        self.assertRaises(sqlite3.OperationalError, self.dbConnection.cursor().execute, f"select * from {TRADESTABLE}")

        self.marketplace.postTrade(self.sampleTrade)

        # Check if table was created with 1 row
        self.assertTrue(len(self.dbConnection.cursor().execute(f"select * from {TRADESTABLE}").fetchall()) == 1)

        # Check if the row has the correct values
        self.assertTrue(self.dbConnection.cursor().execute(f"select * from {TRADESTABLE}").fetchall()[0][0] == Web3.to_checksum_address(self.sampleTrade['collectionAddress']))
        self.assertTrue(self.dbConnection.cursor().execute(f"select * from {TRADESTABLE}").fetchall()[0][1] == Web3.to_checksum_address(self.sampleTrade['src']))
        self.assertTrue(self.dbConnection.cursor().execute(f"select * from {TRADESTABLE}").fetchall()[0][2] == Web3.to_checksum_address(self.sampleTrade['dst']))
        self.assertTrue(self.dbConnection.cursor().execute(f"select * from {TRADESTABLE}").fetchall()[0][3] == self.sampleTrade['token'])
        self.assertTrue(self.dbConnection.cursor().execute(f"select * from {TRADESTABLE}").fetchall()[0][4] == str(self.sampleTrade['price']))
        self.assertTrue(self.dbConnection.cursor().execute(f"select * from {TRADESTABLE}").fetchall()[0][5] == self.sampleTrade['txHash'])
        self.assertTrue(self.dbConnection.cursor().execute(f"select * from {TRADESTABLE}").fetchall()[0][6] == self.sampleTrade['marketplace'])
        # self.assertTrue(self.dbConnection.cursor().execute(f"select * from {TRADESTABLE}").fetchall()[0][7] == str(self.sampleTrade['timestamp']))

        # Check if columns are named correctly
        self.assertTrue(self.dbConnection.cursor().execute(f"select address from {TRADESTABLE}").fetchall()[0][0] == Web3.to_checksum_address(self.sampleTrade['collectionAddress']))
        self.assertTrue(self.dbConnection.cursor().execute(f"select src from {TRADESTABLE}").fetchall()[0][0] == Web3.to_checksum_address(self.sampleTrade['src']))
        self.assertTrue(self.dbConnection.cursor().execute(f"select dst from {TRADESTABLE}").fetchall()[0][0] == Web3.to_checksum_address(self.sampleTrade['dst']))
        self.assertTrue(self.dbConnection.cursor().execute(f"select tokenid from {TRADESTABLE}").fetchall()[0][0] == self.sampleTrade['token'])
        self.assertTrue(self.dbConnection.cursor().execute(f"select price from {TRADESTABLE}").fetchall()[0][0] == str(self.sampleTrade['price']))
        self.assertTrue(self.dbConnection.cursor().execute(f"select txhash from {TRADESTABLE}").fetchall()[0][0] == self.sampleTrade['txHash'])
        self.assertTrue(self.dbConnection.cursor().execute(f"select platform from {TRADESTABLE}").fetchall()[0][0] == self.sampleTrade['marketplace'])
        # self.assertTrue(self.dbConnection.cursor().execute(f"select timestamp from {TRADESTABLE}").fetchall()[0][0] == str(self.sampleTrade['timestamp']))




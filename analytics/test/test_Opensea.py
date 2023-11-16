import unittest
import sqlite3
from analytics.Opensea import Opensea
import asyncio
from web3 import Web3
import os
class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:

        async def helper():
            self.opensea = Opensea(None, self.dbConnection)

        self.dbConnection = sqlite3.connect(':memory:')
        self.w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
        asyncio.run(helper())

        self.takerSingleTxHash = '0x705b74a0b997b561fde249b728951ec9993760db54416f609f0b85d2a6c40a10'
        
        self.takerSingleEvents = self.w3.eth.get_transaction_receipt(self.takerSingleTxHash)['logs'][:2]

    def test_processOpenseaTradeMakerSingle(self):
        pass

    def test_processOpenseaTradeMakerMultiple(self):
        pass

    def test_processOpenseaTradeTakerSingle(self):
        self.opensea.processOpenseaTrade(self.takerSingleEvents[0])
        # for i in self.takerSingleEvents:
        #     x = self.opensea.processOpenseaTrade(i)
            

    def test_processOpenseaTradeTakerMultiple(self):
        pass
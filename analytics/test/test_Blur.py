import unittest
import sqlite3
from analytics.Blur import Blur
import asyncio
from web3 import Web3
import os
class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        async def helper():
            self.blur = Blur(None, self.dbConnection)
        
        self.dbConnection = sqlite3.connect(':memory:')
        self.w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
        asyncio.run(helper())


        
        
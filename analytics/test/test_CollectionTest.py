import unittest
from web3 import Web3  
import os 
from analytics.Collections import Collection
import sqlite3
from request.WebsocketConnect import WsConnect
import asyncio 

class TestCollections(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCollections, self).__init__(*args, **kwargs)
        self.w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))

        self.db = sqlite3.connect(':memory:')

    def test_start(self):
        """
        Test start function of collection
        """
        ws = WsConnect(self.db)
        asyncio.run(ws.connect())
        try:
            c = Collection('0x1A92f7381B9F03921564a437210bB9396471050C', None, self.db)
        except:
            self.fail("Collection constructor raised Exception unexpectedly")

        try:
            asyncio.run(c.start()) 
        except Exception as e:
            self.assertEqual(Exception, e.__class__)
        
    def test_collection_slug_exists(self):
        """
        Check if address exists in the slug relation. 
        If it does not, add it.
        Also add the slug used on opensea and blur as well as the name saved on chain.
        """
        Collection('0x1A92f7381B9F03921564a437210bB9396471050C', None, self.db)

        cursor = self.db.cursor()

        try:
            cursor = self.db.cursor()
            cursor.execute("select * from slug");
            res = cursor.fetchall()
        except:
            self.fail("Could not fetch from slug table")
    
    def test_collection_slug_is_in_db(self):
        Collection('0x1A92f7381B9F03921564a437210bB9396471050C', None, self.db)

        cursor = self.db.cursor()

        try:
            cursor = self.db.cursor()
            cursor.execute("select * from slug where address='0x1A92f7381B9F03921564a437210bB9396471050C'");
            res = cursor.fetchall()
            self.assertEqual(res[0][0], '0x1A92f7381B9F03921564a437210bB9396471050C')
            self.assertEqual(len(res), 1)
        except:
            self.fail("Could not fetch from slug table")

        Collection('0x2acAb3DEa77832C09420663b0E1cB386031bA17B', None, self.db)

        try:
            cursor = self.db.cursor()
            cursor.execute("select * from slug where address='0x2acAb3DEa77832C09420663b0E1cB386031bA17B'");
            res = cursor.fetchall()
            self.assertEqual(res[0][0], '0x2acAb3DEa77832C09420663b0E1cB386031bA17B')
            self.assertEqual(len(res), 1)
        except:
            self.fail("Could not fetch from slug table")

        try:
            cursor = self.db.cursor()
            cursor.execute("select * from slug")
            res = cursor.fetchall()
            self.assertEqual(len(res), 2)
        except:
            self.fail("Could not fetch from slug table")


    def test_collection_validate_address(self):
        """
        Validate address
        """
        self.assertRaises(Exception, Collection, '0x000')

        try:
            Collection('0x1A92f7381B9F03921564a437210bB9396471050C', None, self.db)
        except:
            self.fail("Collection constructor raised Exception unexpectedly")

        



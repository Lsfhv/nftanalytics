import unittest
from web3 import Web3  
import os 
from analytics.Collections import Collection

class TestCollections(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCollections, self).__init__(*args, **kwargs)
        self.w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))

    def test_collection_slug_exists(self):
        """
        Check if address exists in the slug relation. 
        If it does not, add it.
        Also add the slug used on opensea and blur as well as the name saved on chain.
        """
        pass

    def test_collection_validate_address(self):
        """
        Validate address
        """
        self.assertRaises(Exception, Collection, '0x000')

        try:
            Collection('0x1A92f7381B9F03921564a437210bB9396471050C', None)
        except:
            self.fail("Collection constructor raised Exception unexpectedly")

        



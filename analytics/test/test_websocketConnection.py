import unittest
import sqlite3
from request.WebsocketConnect import WsConnect  
import asyncio

class TestWsConnect(unittest.TestCase):
    def __init__(self,*args, **kwargs) -> None:
        super(TestWsConnect, self).__init__(*args, **kwargs)
        self.db = sqlite3.connect(':memory:')
        self.ws = WsConnect()
        asyncio.run(self.ws.connect())  

    
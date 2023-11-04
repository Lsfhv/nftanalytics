"""Tracks the amount of items listed 
within past day/week/month.
"""

from request.getRequest import get
from time import time

from Postgresql import PostgresConnection
from Intervals import intervals, Interval

from datetime import datetime
from sql.sqlQGenerator import insertG, updateG
from time import sleep
from Keys import openseaBaseEndpointV1, openseaBaseEndpointV2, openseaHeaders
from Intervals import HOUR, MINUTE, FIFTEENMINUTES, intervals
import asyncio
from analytics.Transfers import monitorTransfers
from web3 import Web3
import os
from analytics.stats.Volume import computeVolumeMain
from Keys import transferTopic

class Collection:

    def __init__(self, address, ws = None, db = None):
        self.w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))

        if not self.validateAddress(address):
            raise Exception("Invalid address")
        
        self.db = db
        self.address: str = address
        self.retrieveContract = lambda address: f"/asset_contract/{address}"   
        self.ws = ws
        self.slugExists()
        
    def validateAddress(self, address: str) -> bool:
        """Validate address

        Args:
            address (str): address to validate

        Returns:
            bool: whether address is valid
        """

        code = self.w3.eth.get_code(address)
        if code == "0x":
            return False
        return True
        
    async def start(self):
        """
            Start listening to transfer events and computing volumes
        """
        if self.ws == None:
            raise Exception("No ws connection")
        
        await self.ws.sendMessage(self.address, [transferTopic])

        # asyncio.create_task(computeVolumeMain(self.address))
        
    def slugExists(self):
        """
        Check if address exists in the slug relation. 
        If it does not, add it.
        Also add the slug used on opensea and blur as well as the name saved on chain.
        """
        if self.db == None:
            raise Exception("No db connection")

        self.db.cursor().execute(f"create table if not exists slug (address varchar(42) primary key, openseaSlug varchar(100), blurSlug varchar(100), name varchar(100))")

        # response = PostgresConnection().readonly(f"select 1 from slug where address='{self.address}'")
        response = self.db.cursor().execute(f"select 1 from slug where address='{self.address}'").fetchall()
        if len(response) == 0:
            abi = '[{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]'
            openseaSlug =  get(openseaBaseEndpointV1, self.retrieveContract(self.address), headers=openseaHeaders)
            openseaSlug = openseaSlug.json()['collection']['slug']
            w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
            contract = w3.eth.contract(address=self.address, abi = abi)

            name = contract.functions.name().call()

            # No access to blur api yet so just use opensea slug as the blur slug for now.
            # PostgresConnection().insert(f"insert into slug values ('{self.address}', '{openseaSlug}', '{openseaSlug}', '{name}')")
            self.db.cursor().execute(f"insert into slug values ('{self.address}', '{openseaSlug}', '{openseaSlug}', '{name}')") 
            # print(self.db.cursor().execute("select * from slug").fetchall())

        self.db.commit() 

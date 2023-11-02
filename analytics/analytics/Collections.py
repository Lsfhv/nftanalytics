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

    def __init__(self, address, ws):
        self.w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))

        if not self.validateAddress(address):
            raise Exception("Invalid address")
        
        self.address: str = address
        self.retrieveContract = lambda address: f"/asset_contract/{address}"   
        if ws != None:
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
        await self.ws.sendMessage(self.address, [transferTopic])

        asyncio.create_task(computeVolumeMain(self.address))
        
    def slugExists(self):
        """
        Check if address exists in the slug relation. 
        If it does not, add it.
        Also add the slug used on opensea and blur as well as the name saved on chain.
        """

        response = PostgresConnection().readonly(f"select 1 from slug where address='{self.address}'")
        if len(response) == 0:
            abi = '[{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"}]'
            openseaSlug =  get(openseaBaseEndpointV1, self.retrieveContract(self.address), headers=openseaHeaders)
            openseaSlug = openseaSlug.json()['collection']['slug']
            w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
            contract = w3.eth.contract(address=self.address, abi = abi)

            name = contract.functions.name().call()

            # No access to blur api yet so just use opensea slug as the blur slug for now.
            PostgresConnection().insert(f"insert into slug values ('{self.address}', '{openseaSlug}', '{openseaSlug}', '{name}')")
            

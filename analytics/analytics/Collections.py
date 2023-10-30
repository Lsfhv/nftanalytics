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


class Collection:

    def __init__(self, address, chain='ethereum'):
        self.address: str = address
        self.chain: str = chain
        self.delay: Interval = HOUR

        self.retrieveContract = lambda address: f"/asset_contract/{address}"

        self.slugExists()
        
    async def start(self):
        """Start monitoring transfers for this collection.

        """
        asyncio.create_task(monitorTransfers(self.address))

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
            

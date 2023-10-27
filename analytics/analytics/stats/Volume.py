from Postgresql import PostgresConnection
from Intervals import FIFTEENMINUTES, HOUR, DAY, WEEK
from time import time
import asyncio 
from web3 import Web3
import os
import json
from analytics.stats.Holders import computeUniqueOwners

tables = {
    FIFTEENMINUTES: 'fifteenminutesstats', 
    HOUR: 'onedaystats', 
    DAY: 'onehourstats',
    WEEK: 'oneweekstats'
}

def getTotalSupply(address):
    w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
    abi = json.load(open('abis/Erc721Abi.json'))
    contract = w3.eth.contract(address, abi)

    return contract.functions.totalSupply().call()

async def computeVolume(address: str, timeperiod: int):
    """_summary_

    Args:
        address (str): _description_
        timeperiod (int): _description_
    """
    conn = PostgresConnection().connection

    while True:
        uniqueOwners = computeUniqueOwners(address) 
        currentTime = time()

        response = conn.readonly(f"select * from where trades where cast(extract(epoch from time_updated) as bigint) >={currentTime - timeperiod}")

        totalVolume = sum([i[4] for i in response])

        conn.insert(f"insert into {tables[timeperiod]} values ({address}, {totalVolume}, {uniqueOwners}, {getTotalSupply(address)}, {time()})")

        await asyncio.sleep(timeperiod)


async def computeVolumeMain(address:str, intervals: list[int]):
    for i in intervals:
        asyncio.create_task(computeVolume(address, i))
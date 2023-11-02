from Postgresql import PostgresConnection
from Intervals import FIFTEENMINUTES, HOUR, DAY, WEEK, intervals
from time import time
import asyncio 
from web3 import Web3
import os
import json
from analytics.stats.Holders import computeUniqueOwners
import datetime

tables = {
    FIFTEENMINUTES: 'fifteenminutesstats', 
    HOUR: 'onedaystats', 
    DAY: 'onehourstats',
    WEEK: 'oneweekstats'
}

def getTotalSupply(address):
    w3 = Web3(Web3.HTTPProvider(os.environ['INFURAURL']))
    abi = json.load(open('abis/Erc721Abi.json'))
    contract = w3.eth.contract(address, abi =abi)

    try:
        result = contract.functions.totalSupply().call()
    except:
        result = -1
        
    return result
    

async def computeVolume(address: str, timeperiod: int):
    """_summary_

    Args:
        address (str): _description_
        timeperiod (int): _description_
    """

    while True:
        uniqueOwners = computeUniqueOwners(address) 
        currentTime = time()

        response = PostgresConnection().readonly(f"select * from trades where cast(extract(epoch from time_updated) as bigint) >={currentTime - timeperiod} and address='{address}'")

        totalVolume = sum([int(i[4]) for i in response])

        PostgresConnection().insert(f"insert into {tables[timeperiod]} values ('{address}', '{totalVolume}', {uniqueOwners}, {getTotalSupply(address)}, '{str(datetime.datetime.fromtimestamp(int(time())))}')")

        await asyncio.sleep(timeperiod)


async def computeVolumeMain(address:str):
    for i in intervals:
        asyncio.create_task(computeVolume(address, i))
"""
Get the volumes to serve the /volume endpoint.
"""

from Intervals import *
from Postgresql import PostgresConnection
from time import time
import asyncio
import json

async def getVolume(address: str, timePeriod: Interval, ws):
    """
    Get the volume for address over the last timePeriod and send 
    it to the ws.
    """
    while True:
        sql = f"select * from volume where timestep>={time() - timePeriod} and address='{address}'"
        response = PostgresConnection().readonly(sql)
        sum = 0

        for i in response:
            sum += i[1]

        data = {'timeperiod': intervalToString(timePeriod), 'volume': float(sum)}

        data =json.dumps(data)
        ws.send(data)
        await asyncio.sleep(timePeriod)

async def getVolumeMain(address: str, timePeriods: list[str], ws):
    """
    Starts the volume runners. 
    """
    tasks = list(
        map(lambda x : getVolume(address, stringToInterval(x), ws), timePeriods))
    
    await asyncio.gather(*tasks)







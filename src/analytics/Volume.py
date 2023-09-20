"""
Computes the volume over some period of time.
"""
from Postgresql import PostgresConnection
from sql.sqlQGenerator import insertG
from Intervals import FIFTEENMINUTES
import asyncio
from time import time

async def computeVolume(address: str):
    """
    Computes the volume every 15 minutes.
    """

    while True:
        t = time()
        response = PostgresConnection().readonly(f"select ether,weth,blur from transfers where address='{address}' and time_updated >= {t - FIFTEENMINUTES}")

        sum = 0
        for r in response:
            sum += r[0] + r[1] + r[2]

        # print(address, sum, t)
        PostgresConnection().insert(insertG("volume", [address, int(sum), t]))

        await asyncio.sleep(FIFTEENMINUTES)


# 0x8a90cab2b38dba80c64b7734e58ee1db38b8992e 1.279100000000000000 1695201327.999398
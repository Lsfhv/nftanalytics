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

    t = time()

    while True:
        response = PostgresConnection().readonly(f"select ether,weth,blur from transfers where address='{address}' and time_updated >= {t - FIFTEENMINUTES}")

        sum = 0
        for r in response:
            sum += r[0] + r[1] + r[2]

        PostgresConnection().insert(insertG("volume", [address, int(sum), t]))

        t += FIFTEENMINUTES

        await asyncio.sleep(FIFTEENMINUTES)


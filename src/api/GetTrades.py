from Postgresql import PostgresConnection
import asyncio

getTrades = lambda address : PostgresConnection().readonly(f"select * from trades where address='{address}' order by time_updated desc")

async def getTradesMain(websocket, address):
    while True:
        websocket.send(getTrades(address))

        await asyncio.sleep(60)
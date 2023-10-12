from Postgresql import PostgresConnection
import asyncio
import json

getTrades = lambda address : PostgresConnection().readonly(f"select * from trades where address='{address}' order by time_updated desc")

async def getTradesMain(websocket, address):
    while True:
        trades = getTrades(address)
        trades = list(map(lambda x : list(x[:len(x) - 1]) + [x[-1].strftime('%s')], trades))
        trades = json.dumps(trades)

        websocket.send(trades)

        await asyncio.sleep(60)
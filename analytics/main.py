import asyncio
from request.WebsocketConnect import WsConnect
import sqlite3
from analytics.Blur import Blur
from analytics.Opensea import Opensea
monitoring = {}

validAddress = lambda x : True if len(x) == 42 and x[:2] == "0x" else False

async def main():
    dbConnection = sqlite3.connect('test.db')
    x = WsConnect()   
    await x.connect()
    asyncio.create_task(x.startHandlingMessages())

    await Opensea(x, dbConnection).startAll()
    # await Blur(x, dbConnection).startAll() 

    await asyncio.sleep(100000) 
    print('got here ')
        
if __name__ == '__main__':
    asyncio.run(main())
    








    





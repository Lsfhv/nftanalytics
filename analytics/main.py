from sys import argv

from Intervals import *

from analytics.Collections import Collection
import asyncio
from aioconsole import ainput
from analytics.Transfers import monitorTransfers
from analytics.stats.Holders import computeUniqueOwners
from request.WebsocketConnect import WsConnect
import sqlite3

monitoring = {}

validAddress = lambda x : True if len(x) == 42 and x[:2] == "0x" else False

async def main():
    x = WsConnect(sqlite3.connect('test.db'))
    await x.connect()
    asyncio.create_task(x.startHandlingMessages())
    asyncio.create_task(x.startProcessingMessages())
    conn = sqlite3.connect('test.db')

    f = open('input').readlines()
    p = 0
    while p < len(f):
        address = f[p].strip()
        p += 1
        if address not in monitoring:
            
            collection = Collection(address, x, conn)
            monitoring[address] = collection

            asyncio.create_task(collection.start())

        else:
            print("Already monitoring this collection")
    
    await asyncio.create_task(processInput())    

async def processInput():    
    while True:
        address = await ainput("Enter address: ")

        # if validAddress(address):
            
        #     if address not in monitoring:
        #         collection = Collection(address)
        #         monitoring[address] = collection
        #         asyncio.create_task(collection.start())                
        #     else:
        #         print("Already monitoring this collection!") 
        
if __name__ == '__main__':
    asyncio.run(main())
    








    





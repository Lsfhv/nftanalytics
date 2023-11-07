from sys import argv

from Intervals import *

from analytics.Collections import Collection
import asyncio
from aioconsole import ainput
from analytics.Transfers import monitorTransfers
from analytics.stats.Holders import computeUniqueOwners
from request.WebsocketConnect import WsConnect
import sqlite3
from analytics.Marketplace import Marketplace

monitoring = {}

validAddress = lambda x : True if len(x) == 42 and x[:2] == "0x" else False

async def main():
    x = WsConnect(sqlite3.connect('test.db'))   
    await x.connect()
    asyncio.create_task(x.startHandlingMessages())
    asyncio.create_task(x.startProcessingMessages())
    conn = sqlite3.connect('test.db')

    await Marketplace('0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31', x).start()
    # await first.start()
    await Marketplace('0x1d5e12b51dee5e4d34434576c3fb99714a85f57b0fd546ada4b0bddd736d12b2', x).start()
    await Marketplace('0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab', x).start()
    await Marketplace('0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e', x).start()

    # f = open('input').readlines()
    # p = 0
    # while p < len(f):
    #     address = f[p].strip()
    #     p += 1
    #     if address not in monitoring:
            
    #         collection = Collection(address, x, conn)
    #         monitoring[address] = collection

    #         asyncio.create_task(collection.start())

    #     else:
    #         print("Already monitoring this collection")
    
    # await asyncio.create_task(processInput())   
    await asyncio.sleep(1000000) 

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
    








    





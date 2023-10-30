from sys import argv

from Intervals import *

from analytics.Collections import Collection
import asyncio
from aioconsole import ainput
from analytics.Transfers import monitorTransfers
from analytics.stats.Holders import computeUniqueOwners
import analytics.stats.Volume
from request.WebsocketConnect import WsConnect

monitoring = {}

validAddress = lambda x : True if len(x) == 42 and x[:2] == "0x" else False

async def main():
    x = WsConnect()
    await x.connect()
    asyncio.create_task(x.startHandlingMessages())
    asyncio.create_task(x.startProcessingMessages())

    f = open('analytics/input').readlines()
    p = 0
    while p < len(f):
        address = f[p].strip()
        p += 1
        if address not in monitoring:
            
            collection = Collection(address, x)
            monitoring[address] = collection

            asyncio.create_task(collection.start())

        else:
            print("Already monitoring this collection")
    
    await asyncio.create_task(processInput())

async def processInput():
    # x = WsConnect()
    # await x.connect()
    
    # asyncio.create_task(x.startHandlingMessages())
    # asyncio.create_task(x.startProcessingMessages())

    
    # await x.sendMessage('0x1A92f7381B9F03921564a437210bB9396471050C', ['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'])
    # await x.sendMessage('0xE012Baf811CF9c05c408e879C399960D1f305903', ['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'])

    # await x.sendMessage('0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D', ['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'])
    # await x.sendMessage('0xED5AF388653567Af2F388E6224dC7C4b3241C544', ['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'])
    # await x.sendMessage('0x8a90CAb2b38dba80c64b7734e58Ee1dB38B8992e', ['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'])

    
    while True:
        address = await ainput("Enter address: ")

        if validAddress(address):
            
            if address not in monitoring:
                collection = Collection(address)
                monitoring[address] = collection
                asyncio.create_task(collection.start())                
            else:
                print("Already monitoring this collection!") 
        
if __name__ == '__main__':
    asyncio.run(main())








    





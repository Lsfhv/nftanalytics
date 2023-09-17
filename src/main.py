from sys import argv

from Intervals import *

from analytics.Collections import Collection
import asyncio
from aioconsole import ainput
from analytics.Transfers import monitorTransfers

monitoring = {}

async def main():
    f = open('src/input').readlines()
    p = 0
    while p < len(f):
        cmd = f[p].strip()
        slug = f[p + 1].strip()
        address = f[p + 2].strip()
        p += 3
        if slug not in monitoring:
            
            collection = Collection(slug, address)
            monitoring[slug] = collection

            asyncio.create_task(collection.start())

        else:
            print("Already monitoring this collection")
    
    await asyncio.create_task(processInput())

async def processInput():
    while True:
        cmd = await ainput("Enter command: ")

        if cmd == "add":
            slug = await ainput("Enter slug: ")
            
            address = await ainput("Enter address: ")
            
            if slug not in monitoring:
                collection = Collection(slug, address)
                monitoring[slug] = collection
                asyncio.create_task(collection.start())                
            else:
                print("Already monitoring this collection!") 


if __name__ == '__main__':
    asyncio.run(main())
    # asyncio.run(monitorTransfers('0x8821BeE2ba0dF28761AffF119D66390D594CD280'))








    





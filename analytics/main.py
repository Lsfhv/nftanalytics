from sys import argv

from Intervals import *

from analytics.Collections import Collection
import asyncio
from aioconsole import ainput
from analytics.Transfers import monitorTransfers
from analytics.Volume import computeVolume

from analytics.GetVolume import getVolume

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
    # x =  asyncio.run(getVolume('0x8821bee2ba0df28761afff119d66390d594cd280', DAY))
    # print(x)








    




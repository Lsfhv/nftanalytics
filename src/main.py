from sys import argv

from Intervals import *

from analytics.Collections import Collection
import asyncio
from aioconsole import ainput
from analytics.Transfers import monitorTransfers
from analytics.Volume import computeVolume

monitoring = {}

async def main():
    f = open('src/input').readlines()
    p = 0
    while p < len(f):
        cmd = f[p].strip()
        address = f[p + 1].strip()
        p += 2
        if address not in monitoring:
            
            collection = Collection(address)
            monitoring[address] = collection

            asyncio.create_task(collection.start())

        else:
            print("Already monitoring this collection")
    
    await asyncio.create_task(processInput())

async def processInput():
    while True:
        cmd = await ainput("Enter command: ")

        if cmd == "add":

            address = await ainput("Enter address: ")
            
            if address not in monitoring:
                collection = Collection( address)
                monitoring[address] = collection
                asyncio.create_task(collection.start())                
            else:
                print("Already monitoring this collection!") 


if __name__ == '__main__':
    asyncio.run(main())
    # collection = Collection('', '0xED5AF388653567Af2F388E6224dC7C4b3241C544')
    # x =  asyncio.run(getVolume('0x8821bee2ba0df28761afff119d66390d594cd280', DAY))
    # print(x)








    





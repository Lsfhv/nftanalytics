from sys import argv

from intervals import *

from analytics.collection import Collection
from threading import Thread
from multiprocessing import Process
from time import sleep
# import analytics.globalMarket

monitoring = {}

def processInput():
    cmd = input()

    if cmd == "add":
        print("Enter slug and address: ")
        slug = input()
        address = input()
        
        if slug not in monitoring:
            collection = Collection(slug, address)
            monitoring[slug] = collection
            p = Process(target=collection.start)
            p.start()
            
        else:
            print("Already monitoring this collection!") 
    elif cmd == 'plot':
        print("Enter slug: ")
        slug = input()
        collection = monitoring[slug]
        p = Thread(target = collection.plotFloorPrice(MONTH))
        p.start()
    else:
        print('Invalid command')

if __name__ == '__main__':
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
            x = Process(target=collection.start)
            x.start()
        else:
            print("Already monitoring this collection")
    while True:
        processInput()






    





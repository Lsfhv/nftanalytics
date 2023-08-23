from sys import argv

from intervals import *

from analytics.collection import Collection

from multiprocessing import Process
from time import sleep
# import analytics.globalMarket

monitoring = set()

def processInput():
    cmd = input()

    if cmd == "add":
        print("Enter slug and address: ")
        slug = input()
        address = input()
        
        if slug not in monitoring:
            monitoring.add(slug)

            collection = Collection(slug, address)

            p = Process(target=collection.start)
            p.start()
            
        else:
            print("Already monitoring this collection!") 

if __name__ == '__main__':
    f = open('src/input').readlines()
    p = 0
    while p < len(f):
        cmd = f[p].strip()
        slug = f[p + 1].strip()
        address = f[p + 2].strip()
        p += 3
        if slug not in monitoring:
            monitoring.add(slug)
            collection = Collection(slug, address)
            x = Process(target=collection.start)
            x.start()
        else:
            print("Already monitoring this collection")
    sleep(5)
    while True:
        processInput()






    





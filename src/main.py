from sys import argv

from intervals import *

from analytics.collection import Collection

from multiprocessing import Process
from time import sleep
# import analytics.globalMarket

monitoring = set()
collections = []

def monitor(collection):
    while True:
        collection.refresh()

if __name__ == '__main__':
    # Main program loop
    while True:
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




    





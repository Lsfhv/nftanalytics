from sys import argv

from intervals import *

from analytics.collection import Collection

# from multiprocessing import Process
from threading import Thread
from time import sleep

monitoring = set()
collections = []

def monitor(collection):
    while True:
        collection.refresh()
        print("Sleeping for 5 mins ... ")
        sleep(60 * 5)


# Main program loop
while True:
    print("Ready for input: ")
    cmd = input()

    if cmd == "add":
        print("Enter slug and address: ")
        slug = input()
        address = input()

        if slug not in monitoring:
            monitoring.add(slug)

            collection = Collection(slug, address)

            t = Thread(target=monitor, args=[collection])
            t.start()

        else:
            print("Already monitoring this collection!")



    





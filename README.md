# nftanalytics

A background service that collects analytics about NFT collections. 

# How to run

* Get [postgresql](https://www.postgresql.org/) set up on your system
* Provide details so that it can connect to the database at runtime
* Add collections ([opensea](opensea.io) slug and address) that you want to monitor in `input`
* Run with `python3 src/main.py < input` 



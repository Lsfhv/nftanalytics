from sys import argv

from intervals import *

from analytics.collection import Collection


slug = argv[1]
address = argv[2]
chain = argv[3]

# uniqueListings = len(getUniqueListings(slug))

# print(uniqueListings)

# # total = getTotalItems(slug)

# x = listedInPast(SIXHOURS, slug)
# print(x)
# # print(f"{x} listed in past {intervalToString(WEEK)} [{(x/total)*100}]%")

collection = Collection(slug, address)

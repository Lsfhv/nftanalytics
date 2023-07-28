from sys import argv

from intervals import *

from analytics.listedInPast import listedInPast
from analytics.numberListed import getTotalItems



slug = argv[1]
address = argv[2]
chain = argv[3]

total = getTotalItems(slug)

x = listedInPast(WEEK, slug)

print(f"{x} listed in past {intervalToString(WEEK)} [{(x/total)*100}]%")
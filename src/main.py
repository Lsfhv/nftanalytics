from sys import argv

from analytics.floor import getFloor
from analytics.numberListed import getIds
from analytics.numberListed import getListings
from analytics.numberListed import getAllListings


# print("Enter collection slug: ")
# slug = input()

# print("Enter contract address: ")
# address = input()

# print("Enter collection chain: ")
# chain = input()

# # tokenIds = getIds(address, chain)

# # print(tokenIds)

# # x = getListings([8197, 3648], chain, address)

# # print(getAllListings(slug))

# (getAllListings(slug))

slug = argv[1]
address = argv[2]
chain = argv[3]

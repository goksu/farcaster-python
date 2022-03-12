import os

from farcaster.client import FarcasterClient


fcc = FarcasterClient(os.getenv("RINKEBY_NETWORK_ADDR"))

# get user's host address
print(fcc.get_host_addr("v"))

# get user's profile
print(fcc.get_profile("v"))

# get user's casts
print(fcc.get_casts("v"))

import requests

from typing import List
from web3 import Web3

from farcaster.types import Cast, Caster

# w3 = Web3(EthereumTesterProvider())
# w3 = Web3(
#     Web3.HTTPProvider(
#         "https://eth-rinkeby.alchemyapi.io/v2/F3ZVyZvaKR5cDJyJPuh-tSrupGs9myrM"
#     )
# )
# print("w3.isConnected() {}".format(w3.isConnected()))

# Create contract
# REGISTRY_CONTRACT_ADDRESS = "0xe3Be01D99bAa8dB9905b33a3cA391238234B79D1"
# ABI = '[{"name":"getDirectoryUrl","inputs":[{"internalType":"bytes32","name":"username","type":"bytes32"}],"outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"addressToUsername","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}]'
# fc_registry_contract = w3.eth.contract(address=REGISTRY_CONTRACT_ADDRESS, abi=ABI)
# print(Web3.toBytes("v"))
# print(fc_registry_contract.caller().getDirectoryUrl)
# print(type(Web3.toBytes(text="v")))
# print(type("v".encode("utf-8")))
# directory_url = fc_registry_contract.caller().getDirectoryUrl("v".encode("utf-8"))
# print("directory_url: {}".format(directory_url))


class FarcasterClient:
    # Farcaster registry Rinkeby contract addr
    __REGISTRY_CONTRACT_ADDRESS = "0xe3Be01D99bAa8dB9905b33a3cA391238234B79D1"
    # Farcaster registry ABI
    __ABI = '[{"name":"getDirectoryUrl","inputs":[{"internalType":"bytes32","name":"username","type":"bytes32"}],"outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"addressToUsername","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}]'

    # Web3.HTTPProvider(
    #     "https://eth-rinkeby.alchemyapi.io/v2/F3ZVyZvaKR5cDJyJPuh-tSrupGs9myrM"
    # )

    def __init__(self, rinkeby_network_conn_str: str):
        web3_provider = Web3.HTTPProvider(rinkeby_network_conn_str)
        self.w3 = Web3(web3_provider)
        self.registry = self.w3.eth.contract(
            address=self.__REGISTRY_CONTRACT_ADDRESS, abi=self.__ABI
        ).caller()

    def get_profile(self, username: str) -> Caster:
        host_addr = self.get_host_addr(username)
        response = requests.get(host_addr).json()
        return Caster(
            hash=response["merkleRoot"],
            display_name=response["body"]["displayName"],
            activity_url=response["body"]["addressActivityUrl"],
        )

    def get_casts(self, username: str) -> List[Cast]:
        caster = self.get_profile(username)
        response = requests.get(caster.activity_url).json()
        return [
            Cast(hash=r["merkleRoot"], content=r["body"]["data"]["text"])
            for r in response
        ]

    def get_host_addr(self, username: str) -> str:
        encoded_username = Web3.toBytes(text=username)
        return self.registry.getDirectoryUrl(encoded_username)


# fcc = FarcasterClient(
#     Web3.HTTPProvider(
#         "https://eth-rinkeby.alchemyapi.io/v2/F3ZVyZvaKR5cDJyJPuh-tSrupGs9myrM"
#     )
# )

# print(fcc.get_host_addr("v"))
# print(fcc.get_host_addr("gt"))
# print("get_casts", fcc.get_casts("gt"))
# "https://eth-rinkeby.alchemyapi.io/v2/F3ZVyZvaKR5cDJyJPuh-tSrupGs9myrM"

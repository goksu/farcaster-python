import requests

from typing import List
from web3 import Web3

from farcaster.types import Cast, Caster


class FarcasterClient:
    # Farcaster registry Rinkeby contract addr
    __REGISTRY_CONTRACT_ADDRESS = "0xe3Be01D99bAa8dB9905b33a3cA391238234B79D1"
    # Farcaster registry ABI
    __ABI = '[{"name":"getDirectoryUrl","inputs":[{"internalType":"bytes32","name":"username","type":"bytes32"}],"outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"addressToUsername","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}]'

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

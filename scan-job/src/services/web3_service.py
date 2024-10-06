from web3 import Web3
from web3.middleware import geth_poa_middleware
import json


class Web3Service:
    @classmethod
    def __init__(self, http_provider: str):
        self.web3 = Web3(Web3.HTTPProvider(http_provider))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    @classmethod
    def get_contract(self, contract_address: str, abi):
        return self.web3.eth.contract(
            address=contract_address, abi=abi)

    # AttributeDict({'args': AttributeDict({'proID': b'fejwoicmaow7Cy\x1a\x18\x87\x99O\x15Lf\xce\xa1gl&;,wg?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00a', 'round': 'PUBLICSALE', 'from': '0x43791A1887994f154C66cEa1676C263b2C77673F', 'amountToken': 1000000000000000000, 'price': 1655116272851818}),
    #               'event': 'BuyToken', 'logIndex': 20, 'transactionIndex': 2, 'transactionHash': HexBytes('0xa94be4d590903a48f20be8aa5dbac566b5f5a3678ceca083d539335ef1003783'), 'address': '0x9f3D7e9e295C5D5eb588496A8c81b65631CF4AC2', 'blockHash': HexBytes('0x963a326cf1cb431bde446c9826109b87eabdccc948a00033b418c761f79acf26'), 'blockNumber': 41271963})
    @classmethod
    def parse_event_data(self, contract, to_block_number: int, current_block_number: int, event_name: str):
        list_event_data = contract.events[event_name].get_logs(
            fromBlock=current_block_number,
            toBlock=to_block_number,
        )

        if len(list_event_data) <= 0:
            return None

        return list_event_data

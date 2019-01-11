import web3
from web3 import Web3, HTTPProvider

# Stubs for eval()

def AttributeDict(self):
    return self

def HexBytes(self):
    return self

server = Web3(HTTPProvider("https://sokol.poa.network/"))

contractAddress = server.toChecksumAddress('0xe87a3686b0a42d66eee76d48c9a8307c27d14d1c')
contractABI = [{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"withdraw","inputs":[{"type":"uint256","name":"_value"}],"constant":False},{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"transfer","inputs":[{"type":"bytes32","name":"_txHash"},{"type":"uint256","name":"_vout"},{"type":"address[]","name":"_recipients"},{"type":"uint256[]","name":"_values"}],"constant":False},{"type":"constructor","stateMutability":"nonpayable","payable":False,"inputs":[]},{"type":"fallback","stateMutability":"payable","payable":True},{"type":"event","name":"Transfer","inputs":[{"type":"bytes32","name":"tx_source","indexed":True},{"type":"bytes32","name":"tx_address","indexed":True},{"type":"address","name":"recipient","indexed":True},{"type":"uint256","name":"value","indexed":False},{"type":"uint256","name":"vout","indexed":False}],"anonymous":False}]

contract = server.eth.contract(address=contractAddress, abi=contractABI)

eventFilter = contract.events.Transfer.createFilter(fromBlock=0, toBlock='latest')
log = eventFilter.get_all_entries()

for index in range(len(log)):
    log[index] = eval(str(log[index]))

eventLog = open("eventLog.txt", "w+")

for event in log:
    eventLog.write(str(event) + "\n")

eventLog.close()

'''
returns:
{
    'args': {
            'tx_source': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            'tx_address': b"\x93\xcdp\xa0f'\xb14+\x9f\xc3\x97\xa0\x8e\xe6\x9b\xe9\x16L\x91\x06\xcc\x1cG~\xbb\xb2#P\x0cii",
            'recipient': '0x2eD61BCA22E097506FCd9Eb1A0C5256a1f974604',
            'value': 3617920,
            'vout': 0
    },
    'event': 'Transfer',
    'logIndex': 0,
    'transactionIndex': 1,
    'transactionHash': '0x75be2017e3c874d1a517d90f7aa5ecab0867e962e9bfda1412aac00f6d1250d4',
    'address': '0xe87A3686B0A42d66EEe76D48c9A8307c27D14D1c',
    'blockHash': '0x4eab261d16e9221b3e482c8d52268e51a816cbf69f23e9d4e0a23fcc3ac15ddb',
    'blockNumber': 6070845
}
'''

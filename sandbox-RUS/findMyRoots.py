import web3
from web3 import Web3, HTTPProvider
server = Web3(HTTPProvider("https://sokol.poa.network/"))

# Clean tx's receipt

def AttributeDict(self):
    return self

def HexBytes(self):
    return self

def filteredTX(tx):
    return eval(tx[14:-1])

class User(object):
    def __init__(self, address):
        self.address = address
        self.rootTokens = []
    def findRoot(self, eventLogs):


user = User(input("Your address: "))

parent = user.account
used = {} # key is address,
blocks = []
global blocks
def dfs(used, current): # current = node address

    used[current] = 1
    senders = []
    for event in eventLogs:
        tx = filteredTX(server.eth.getTransaction(event['transactionHash']))
        if event['args']['tx_source'] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            BN = tx['blockNumber']
            blocks.append(BN)
        if event['args']['recipient'] == current:
            sender = tx['from']
            senders += sender
    for sender in senders:
        if used[sender] == None:
            dfs(used, sender)
print(blocks)

'''
EL example
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

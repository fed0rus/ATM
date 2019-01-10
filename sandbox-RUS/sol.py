from web3 import Web3, HTTPProvider

def HexBytes(self):
    return self

server = Web3(HTTPProvider("https://sokol.poa.network/"))
rawLog = open("shit.txt", 'r')
log = eval(rawLog.read())

userAddress = input("User address:\t")
blocks = []

for k in range(len(log)):
    txReceipt =

# LOG::EXAMPLE
'''
{
    'address': '0xe87A3686B0A42d66EEe76D48c9A8307c27D14D1c',
    'blockHash': '0x4eab261d16e9221b3e482c8d52268e51a816cbf69f23e9d4e0a23fcc3ac15ddb',
    'blockNumber': 6070845,
    'data': '0x00000000000000000000000000000000000000000000000000000000003734800000000000000000000000000000000000000000000000000000000000000000',
    'logIndex': 0,
    'removed': False,
    'topics': ['0x1c38707f89a97389446643750be803fe897ac1f6b841a1305c94fc19bed93348', '0x0000000000000000000000000000000000000000000000000000000000000000', '0x93cd70a06627b1342b9fc397a08ee69be9164c9106cc1c477ebbb223500c6969', '0x0000000000000000000000002ed61bca22e097506fcd9eb1a0c5256a1f974604'],
    'transactionHash': '0x75be2017e3c874d1a517d90f7aa5ecab0867e962e9bfda1412aac00f6d1250d4',
    'transactionIndex': 1,
    'transactionLogIndex': '0x0',
    'type': 'mined'
}
'''
# TX::EXAMPLE

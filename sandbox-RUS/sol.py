from web3 import Web3, HTTPProvider

def HexBytes(self):
    return self

server = Web3(HTTPProvider("https://sokol.poa.network/"))
rawLog = open("shit.txt", 'r')
log = eval(rawLog.read())

fullLog = []
# userAddress = input("User address:\t")
blocks = []

print("Gathering data...")

for k in range(len(log)):
    txReceipt = eval(str(server.eth.getTransaction(log[k]['transactionHash']))[14:-1])
    fullLog.append(txReceipt)
    print(str(k) + " done")

file = open("fullLog.txt", 'w+')
file.write(str(fullLog))
file.close()


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
'''
RETURNS
{
    'blockHash': HexBytes('0x4eab261d16e9221b3e482c8d52268e51a816cbf69f23e9d4e0a23fcc3ac15ddb'),
    'blockNumber': 6070845,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0x2eD61BCA22E097506FCd9Eb1A0C5256a1f974604',
    'gas': 300000,
    'gasPrice': 1000000000,
    'hash': HexBytes('0x75be2017e3c874d1a517d90f7aa5ecab0867e962e9bfda1412aac00f6d1250d4'),
    'input': '0x',
    'nonce': 0,
    'publicKey': HexBytes('0xd2d8042201b0fb87d37d853913ec6b9837ace53c0c8bad9efa39630da6aceac6d44c09a2832064e1e76220da750f3c964c93c1119c6a34390f4e3a6ca16617cf'),
    'r': HexBytes('0x8c28663744392a5bba159878974ee67289501af5eeb45b9927f5348cee20c187'),
    'raw': HexBytes('0xf86780843b9aca00830493e094e87a3686b0a42d66eee76d48c9a8307c27d14d1c83373480801ca08c28663744392a5bba159878974ee67289501af5eeb45b9927f5348cee20c187a03f984d0234fe78c3b9e2bcfab723506b592c182145723ec2c6fb30248ef7665c'),
    's': HexBytes('0x3f984d0234fe78c3b9e2bcfab723506b592c182145723ec2c6fb30248ef7665c'),
    'standardV': 1,
    'to': '0xe87A3686B0A42d66EEe76D48c9A8307c27D14D1c',
    'transactionIndex': 1,
    'v': 28,
    'value': 3617920
}
'''

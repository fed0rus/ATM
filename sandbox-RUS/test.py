import web3
from web3 import Web3, HTTPProvider
server = Web3(HTTPProvider("https://sokol.poa.network/"))
print(server.eth.getTransaction('0x75be2017e3c874d1a517d90f7aa5ecab0867e962e9bfda1412aac00f6d1250d4'))

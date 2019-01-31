from web3 import Web3, HTTPProvider

server = Web3(HTTPProvider("https://sokol.poa.network/"))

print(server.eth.blockNumber)

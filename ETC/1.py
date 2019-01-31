from web3 import Web3, HTTPProvider

server = Web3(HTTPProvider("https://sokol.poa.network"))

privateKey = bytes.fromhex(input("Private key: "))

userAddress = server.personal.importRawKey(privateKey, '')

print(server.personal.))

--rpcapi "eth,net,web3,personal"
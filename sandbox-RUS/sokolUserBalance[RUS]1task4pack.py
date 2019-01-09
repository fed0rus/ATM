# Stages:
# 0 [DONE]   Configure the host [SKL]
# 1 [INPR]   Generate privateKey
# 2 [INPR]   Generate address
# 3 [AWAT]   Send a request to the Sokol server and receive the fucking account!

import web3
from web3 import Web3, HTTPProvider
from eth_account import Account

class User(object):
    def __init__(self, UUID, PIN):
        self.UUID = str(UUID)
        self.PIN = str(PIN)

    def extractPIN(self):
        return [int(k) for k in self.PIN]

    def extractUUID(self):
        return (self.UUID).replace('-', '')

    def generatePrivateKey(self):
        UUID = self.extractUUID()
        PIN = self.extractPIN()
        print("-----------------------------")
        print("\t\tTesting field")
        privateKey = Web3.soliditySha3(["bytes16"], [b''])
        for k in range(4):
            privateKey = Web3.soliditySha3(["bytes16", "bytes16", "int8"], [privateKey, UUID.encode("utf-8"), PIN[k]]) # ABI-packed, keccak256 hashed
        print("\n-----------------------------")
        self.privateKey = privateKey

    def generateAddress(self):
        account = Account.privateKeyToAccount(self.privateKey)
        self.address = account.address

# Stage 0

server = Web3(HTTPProvider("https://sokol.poa.network/"))

# Stage 1

UUID = input()
PIN = input()
user = User(UUID, PIN)
user.generatePrivateKey()
print("-----------------------------")

print("\t\tAnswer field\n")

# Stage 2

user.generateAddress()
print("Address: ", user.address) # WRONG!

# Stage 3

print("Amount:  ", server.eth.getBalance(user.address))

print("-----------------------------")
# Sandbox

'''
[TI]
a52b5033-35d1-4aa6-8190-72f0116edba3
1741
[TO]
0x16d3F647d12853DFae28015DBdbD392AFff33Ce6
0

[AFTER CHANGING BYTES METHOD TO UNCODE("UTF-8")]
'''
# hashfunc works OK

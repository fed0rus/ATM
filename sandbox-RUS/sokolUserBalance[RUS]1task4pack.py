# Stages:
# 0 [DONE]   Configure the host [SKL]
# 1 [DONE]   Generate privateKey
# 2 [INPR]   Generate address
# 3 [AWAT]   Send a request to the Sokol server and receive the fucking account!

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
        privateKey = Web3.soliditySha3(["bytes32"], [b''])
        for k in range(4):
            privateKey = Web3.soliditySha3(["bytes32", "bytes16", "int8[]"], [privateKey, bytearray.fromhex(UUID), [PIN[k]]]) # ABI-packed, keccak256 hashed
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

# Stage 2

user.generateAddress()
print(user.address)
print((Web3.soliditySha3(["bytes32"], ["Ethereum is a distributed database".encode("utf-8")])).hex())

'''
a52b5033-35d1-4aa6-8190-72f0116edba3
1741
'''

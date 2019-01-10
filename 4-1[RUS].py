# Stages:
# 0 [DONE]   Configure the host [SKL]
# 1 [DONE]   Generate privateKey
# 2 [DONE]   Generate address
# 3 [DONE]   Send a request to the Sokol server and receive the fucking account!
# 4 [INPR]   Be happy

import web3
from web3 import Web3, HTTPProvider
from eth_account import Account

class User(object):
    def __init__(self, UUID, PIN):
        self.UUID = "0x" + str(UUID)
        self.PIN = str(PIN)

    def extractPIN(self):
        return [int(k) for k in self.PIN]

    def extractUUID(self):
        return (self.UUID).replace('-', '')

    def generatePrivateKey(self):
        UUID = self.extractUUID()
        PIN = self.extractPIN()
        privateKey = Web3.soliditySha3(["bytes16"], [b''])
        for k in range(4):
            privateKey = Web3.soliditySha3(["bytes16", "bytes16", "int8"], [privateKey, UUID, PIN[k]]) # ABI-packed, keccak256 hashed
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

print("\t\tSokol Testnet\n")

# Stage 2

user.generateAddress()
print("Address: ", user.address)

# Stage 3

print("Credit:  ", server.eth.getBalance(user.address))

print("-----------------------------")
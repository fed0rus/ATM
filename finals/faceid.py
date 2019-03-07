#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse
from eth_account import Account

class User(object):

    def __init__(self, UUID, PIN):
        self.UUID = "0x" + str(UUID.replace('-', ''))
        self.PIN = str(PIN)

    def setServer(self, server):
        self.server = server

    def extractPIN(self):
        return [int(k) for k in self.PIN]

    def generatePrivateKey(self):
        UUID = self.UUID
        PIN = self.extractPIN()
        privateKey = server.solidityKeccak(["bytes16"], [b''])
        for k in range(4):
            privateKey = Web3.solidityKeccak(["bytes16", "bytes16", "int8"], [privateKey, UUID, PIN[k]]) # ABI-packed, keccak256 hashed
        self.privateKey = privateKey

    def generateAddress(self):
        account = Account.privateKeyToAccount(self.privateKey)
        self.address = account.address

def scaleValue(value):
    p = ['wei', 'kwei', 'mwei', 'gwei', 'szabo', 'finney', 'poa']
    nowp = 0
    while (value >= 1000 and nowp < 6):
        value /= 1000
        nowp += 1
    return str(round(value, 6)) + ' ' + p[nowp]

def setArgs():

    parser = argparse.ArgumentParser()
    parser.add_argument("--balance", action="store", help="Get the balance of your account")
    args = parser.parse_args()
    return vars(args)

def getBalanceByID(server):
    try:
        with open("person.json", 'r') as person:
            data = json.load(person)
            id = str(data["id"])
        PIN = args["balance"]
        user = User(id, PIN)
        user.setServer(server)
        user.generatePrivateKey()
        user.generateAddress()
        balance = scaleValue(server.eth.getBalance(user.address))
        print("Your balance is {}".format(balance))
    except:
        print("ID is not found")

if __name__ == "__main__":

    args = setArgs()

    if args["balance"] is not None:
        server = Web3(HTTPProvider("https://sokol.poa.network"))
        getBalanceByID(server)

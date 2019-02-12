#!/usr/bin/env python

# WARNING! You can adjust the `speed` parameter when initialize a `gasPrice` variable

# In case of testing in terminal, uncomment the following 2 lines and change the path to used libs
import sys
sys.path.append("C:\Python_Interpreter\Lib\site-packages")

from web3 import Web3, HTTPProvider
from eth_account import Account
import requests
import argparse


class User(object):
    def __init__(self, keyNoPrefix):
        self.generateAddressFromKey(keyNoPrefix)

    def generateAddressFromKey(self, keyNoPrefix):
        privateKey = "0x" + str(keyNoPrefix)
        self.privateKey = privateKey
        self.address = str((Account.privateKeyToAccount(privateKey)).address)

    def getBalance(self):
        return server.eth.getBalance(self.address)

    def configureTx(self, to, value):
        txJSON = dict()
        txJSON["nonce"] = server.eth.getTransactionCount(self.address)
        txJSON['gasPrice'] = gasPrice
        txJSON['gas'] = 30000
        txJSON['to'] = to
        txJSON['value'] = value # add scaling
        return txJSON

    def sendTx(self, to, value):
        txJSON = self.configureTx(to, value)
        signedTx = server.eth.account.signTransaction(self.configureTx(to, value), self.privateKey)
        return server.eth.sendRawTransaction(signedTx.rawTransaction)


# main functions

def printBalance(account):
    print("Balance on \"{address}\" is {val}".format(address=account.address[2:], val=scaleValue(account.getBalance())))

def printTransaction(to, value):
    if account.getBalance() < value:
        print("No enough funds for payment")
    else:
        txHash = account.sendTx(to, value)
        print("Payment of {val} to {addr} scheduled".format(val=str(scaleValue(value)), addr=to[2:]))
        print("Transaction Hash: " + str(txHash.hex()))

def printTxStatus(txHash):
    receipt = cleanTxResponse(server.eth.getTransaction(txHash))
    print(receipt)
    if receipt is None:
        print("No such transaction in the chain")
    elif receipt["blockHash"] is None:
        print("Delay in payment of {val} to {addr}".format(val=scaleValue(receipt["value"]), addr=(receipt["to"])[2:]))
    else:
        print("Payment of {val} to {addr} confirmed".format(val=scaleValue(receipt["value"]), addr=(receipt["to"])[2:]))

# utils

def HexBytes(value):
    return value

def cleanTxResponse(rawReceipt):
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

def scaleValue(value):
    if value < 1e3:
        return str(value) + " wei"
    elif 1e3 <= value < 1e6:
        val = float("{:.6f}".format((float(value) / 1e3)))
        return str(int(val)) + " kwei" if val - int(val) == 0 else str(val) + " kwei"
    elif 1e6 <= value < 1e9:
        val = float("{:.6f}".format((float(value) / 1e6)))
        return str(int(val)) + " mwei" if val - int(val) == 0 else str(val) + " mwei"
    elif 1e9 <= value < 1e12:
        val = float("{:.6f}".format((float(value) / 1e9)))
        return str(int(val)) + " gwei" if val - int(val) == 0 else str(val) + " gwei"
    elif 1e12 <= value < 1e15:
        val = float("{:.6f}".format((float(value) / 1e12)))
        return str(int(val)) + " szabo" if val - int(val) == 0 else str(val) + " szabo"
    elif 1e15 <= value < 1e18:
        val = float("{:.6f}".format((float(value) / 1e15)))
        return str(int(val)) + " finney" if val - int(val) == 0 else str(val) + " finney"
    else:
        val = float("{:.6f}".format((float(value) / 1e18)))
        return str(int(val)) + " poa" if val - int(val) == 0 else str(val) + " poa"

# setting up the gas price


def getGasPrice(speed):
    response = requests.get("https://gasprice.poa.network")
    return int((response.json())[speed] * 1e9)


def initParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", help="User's private key")
    parser.add_argument("-t", "--to", help="Recipient of the transaction")
    parser.add_argument("-v", "--value", help="Amount of value in wei")
    parser.add_argument("-T", "--tx", help="Transaction hash")
    global args
    args = parser.parse_args()
    args = vars(args)


server = Web3(HTTPProvider("https://sokol.poa.network"))
global gasPrice
gasPrice = getGasPrice(speed="slow")

initParser()

# determining proper action

if args["tx"] is None and args["to"] is None:
    account = User(args["key"])
    printBalance(account)

elif args["tx"] is None:
    account = User(args["key"])
    printTransaction("0x" + str(args["to"]), int(args["value"]))

elif args["key"] is None and args["value"] is None:
    printTxStatus(args["tx"])

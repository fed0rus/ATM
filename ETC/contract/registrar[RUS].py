import sys
sys.path.append("C:\Solc")
sys.path.append("C:\Python_Interpreter\Lib\site-packages")

import json
from solc import compile_source
from web3 import Web3, HTTPProvider
import argparse
from eth_account import Account

def extractPrivateKey():
    account = open("account.json", 'r')
    privateKey = eval(account.read())["account"]
    account.close()
    return privateKey

def generateAddressFromPrivateKey(privateKey):
    privateKey = "0x" + str(privateKey)
    return str((Account.privateKeyToAccount(privateKey)).address)

def generateContract():
    privateKey = extractPrivateKey()
    contractOwnerAddress = generateAddressFromPrivateKey(privateKey)
    source = '''
    ''' % (contractOwnerAddress, contractOwnerAddress)
    compiledSource = compile_source(source)
    contractInterface = compiledSource["<stdin>:KYC"]
    Contract = server.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
    pass
def main():
    server = Web3(HTTPProvider("https://sokol.poa.network"))
    generateContract()

if __name__ == "__main__":
    main()

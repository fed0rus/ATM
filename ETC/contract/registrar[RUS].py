import sys
sys.path.append("C:\Solc")
sys.path.append("C:\Python_Interpreter\Lib\site-packages")

import json
from solc import compile_source

def getPrivateKey():
    account = open("account.json", 'r')
    privateKey = eval(account.read())["account"]
    account.close()
    return privateKey

def generateContract(contractOwnerAddress):
    source = '''
    PUT CONTRACT KYC CODE HERE
    ''' % (contractOwnerAddress, contractOwnerAddress)
    compiledSource = compile_source(source)
    contractInterface = compiledSource["<stdin>:KYC"]

def main():
    server = Web3(HTTPProvider("https://sokol.poa.network"))

print(generateContract())

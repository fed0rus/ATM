import sys
sys.path.append("C:\Solc")
sys.path.append("C:\Python_Interpreter\Lib\site-packages")

from eth_abi import encode_abi
import json
import requests
from solc import compile_source
from web3 import Web3, HTTPProvider
import argparse
from eth_account import Account

class Owner(object):
    def __init__(self, address, privateKey):
        self.address = address
        self.privateKey = privateKey
    def addContract(self, contract):
        self.possessedContract = contract

def extractPrivateKey():
    account = open("account.json", 'r')
    privateKey = eval(account.read())["account"]
    account.close()
    return privateKey

def generateAddressFromPrivateKey(privateKey):
    privateKey = "0x" + str(privateKey)
    return str((Account.privateKeyToAccount(privateKey)).address)

def retrieveContractSourceCode(ownerAddress):
    soliditySource = '''
    pragma solidity ^0.4.24;

    contract Mortal {
        address owner;

        constructor() public {
            require(%s != address(0));
            owner = %s;
        }

        modifier ownerOnly {
            require(msg.sender == owner);
            _;
        }
    }

    contract KYC is Mortal {

        mapping (address => string) addressToCustomerName;
        mapping (string => address) customerNameToAddress;

        function addCustomer(string memory customerName) public {
            require(msg.sender != address(0));
            addressToCustomerName[msg.sender] = customerName;
            customerNameToAddress[customerName] = msg.sender;
        }

        function deleteCustomer() public {
            addressToCustomerName[msg.sender] = '';
        }

        function retrieveName(address customerAddress) public returns (string memory) {
            return addressToCustomerName[customerAddress];
        }

        function retrieveAddress(string memory customerName) public returns (address) {
            return customerNameToAddress[customerName];
        }

        function () external payable {}

        function deleteContract() public ownerOnly {
            selfdestruct(address(owner));
        }
    }
    ''' % (ownerAddress, ownerAddress)
    return soliditySource

# utils

HexBytes = lambda x: x

def getGasPrice(speed):
    response = requests.get("https://gasprice.poa.network")
    return int((response.json())[speed] * 1e9)

def cleanTxResponse(rawReceipt):
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

# essential

def deployContract(server, owner):
    contractData = {}
    contractSource = retrieveContractSourceCode(owner.address)
    compiledSource = compile_source(contractSource)
    contractInterface = compiledSource["<stdin>:KYC"]
    contractData["abi"] = contractInterface['abi']
    rawKYC = server.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
    gasCost = server.eth.estimateGas({"to": None, "value": 0, "data": rawKYC.bytecode})
    tx = {
        "nonce": server.eth.getTransactionCount(owner.address),
        "gasPrice": getGasPrice(speed="fast"),
        "gas": gasCost,
        "to": None,
        "value": 0,
        "data": rawKYC.bytecode
    }
    contractDeploymentTransactionSigned = server.eth.account.signTransaction(
        tx,
        extractPrivateKey()
    )
    deploymentHash = server.eth.sendRawTransaction(contractDeploymentTransactionSigned.rawTransaction)
    txReceipt = server.eth.waitForTransactionReceipt(deploymentHash)
    contractData["contractAddress"] = cleanTxResponse(txReceipt)["contractAddress"]
    contract = server.eth.contract(
        address=contractData["contractAddress"],
        abi=contractData["abi"],
    )
    file = open("database.json", "w+")
    startBlock = cleanTxResponse(txReceipt)["blockNumber"]
    dataToStore = {
        "registrar": contract.address,
        "startBlock": startBlock,
    }
    file.write(str(dataToStore))
    file.close()
    return contract

def invokeContract(server, sender, contract, methodSig, methodName, methodArgs, methodArgsTypes, value=0):

    methodSignature = server.sha3(text=methodSig)[0:4].hex()
    params = encode_abi(methodArgsTypes, methodArgs)
    payloadData = "0x" + methodSignature + params.hex()
    estimateData = {
        "to": contract.address,
        "value": value,
        "data": payloadData
    }
    rawTX = {
        "to": contract.address,
        "data": payloadData,
        "value": value,
        "from": sender.address,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gasPrice": getGasPrice(speed="fast"),
    }
    gas = server.eth.estimateGas(rawTX)
    rawTX["gas"] = gas
    signedTX = server.eth.account.signTransaction(
        rawTX,
        sender.privateKey,
    )
    txHash = server.eth.sendRawTransaction(signedTX.rawTransaction).hex()
    return txHash

def callContract(contract, methodName, methodArgs):
    args = str(methodArgs)[1:-1]
    response = eval("contract.functions.{}({}).call()".format(methodName, args))
    print(response)

def initParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("-a", "--add", action="store", help="Bind your name with current address in the KYC contract")

    global args
    args = parser.parse_args()

def handleArgs(server, owner):
    if args.deploy is True:
        contract = deployContract(server, owner)
        owner.addContract(contract)
        print("Contract address: {0}".format(contract.address))
    elif args.add is not None:
        # fetch contract address from database.json
        db = open("database.json", 'r')
        data = eval(db.read())
        db.close()
        contractAddress = data["registrar"]
        # generate contract abi
        contractSource = retrieveContractSourceCode(owner.address)
        compiledSource = compile_source(contractSource)
        contractInterface = compiledSource["<stdin>:KYC"]
        _abi = contractInterface['abi']
        _contract = server.eth.contract(address=contractAddress, abi=_abi)
        txHash = invokeContract(
            server=server,
            sender=owner,
            contract=_contract,
            methodSig="addCustomer(string)",
            methodName="addCustomer",
            methodArgs=[str(args.add)],
            methodArgsTypes=["string"],
        )
        if len(txHash) == 66:
            print("Successfully added by {tx}".format(tx=txHash))
        else:
            print("Error")

def main():
    initParser()
    server = Web3(HTTPProvider("https://sokol.poa.network"))
    owner = Owner(generateAddressFromPrivateKey(extractPrivateKey()), extractPrivateKey())
    handleArgs(server, owner)

if __name__ == "__main__":
    main()

# cd Documents/github/fintech/etc/contract

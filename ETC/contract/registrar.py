import sys
sys.path.append("C:\Solc")
sys.path.append("C:\Python_Interpreter\Lib\site-packages")

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

def extractPrivateKey():
    account = open("account.json", 'r')
    privateKey = eval(account.read())["account"]
    account.close()
    return privateKey

def generateAddressFromPrivateKey(privateKey):
    privateKey = "0x" + str(privateKey)
    return str((Account.privateKeyToAccount(privateKey)).address)

def retrieveContractSourceCode(potentialOwnerAddress):
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
    ''' % (potentialOwnerAddress, potentialOwnerAddress)
    return soliditySource

# utils

def getGasPrice(speed):
    response = requests.get("https://gasprice.poa.network")
    return int((response.json())[speed] * 1e9)

HexBytes = lambda x: x

def cleanTxResponse(rawReceipt):
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

# essential

def generateContract(server, contractOwnerAddress):
    contractData = {}
    contractSource = retrieveContractSourceCode(contractOwnerAddress)
    compiledSource = compile_source(contractSource)
    contractInterface = compiledSource["<stdin>:KYC"]
    contractData["abi"] = contractInterface['abi']
    rawKYC = server.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
    gasCost = server.eth.estimateGas({"to": None, "value": 0, "data": rawKYC.bytecode})
    tx = {
        "nonce": server.eth.getTransactionCount(contractOwnerAddress),
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
    return contractData

def invokeContract(server, sender, contract, functionNameSig, functionName, functionArgs, value=0):
    methodSignature = server.sha3(text=functionNameSig)[0:4].hex()
    print("sig: ", methodSignature)
    params = ""
    for param in functionArgs:
        if type(param) == int:
            params += param.to_bytes(32, byteorder="big").hex()
            print("paramINT: ", param.to_bytes(32, byteorder="big").hex())
        elif type(param) == str:
            params += param.encode("utf-8").hex()
            print("paramSTR: ", param.encode("utf-8").hex())
    payloadData = "0x" + methodSignature + params
    print("Payload: ", payloadData)
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
        "gas": 100000,
        # "gas": eval("contract.functions.{}.estimateGas(estimateData)".format(functionName)),
        "gasPrice": getGasPrice(speed="fast")
    }
    signedTX = server.eth.account.signTransaction(
        rawTX,
        sender.privateKey
    )
    txReceipt = server.eth.sendRawTransaction(signedTX.rawTransaction)
    return txReceipt

def main():
    # server = Web3(HTTPProvider("https://sokol.poa.network"))
    # owner = Owner(generateAddressFromPrivateKey(extractPrivateKey()), extractPrivateKey())
    # # # contractData = generateContract(server, contractOwnerAddress)
    # contractData = {'abi': [{'constant': False, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'retrieveName', 'outputs': [{'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'string'}], 'name': 'addCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteContract', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'string'}], 'name': 'retrieveAddress', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'}], 'contractAddress': '0xd49cf73edD179cfc33E7220d158895E2f13fCe51'}
    # KYC = server.eth.contract(address=contractData["contractAddress"], abi=contractData["abi"])
    # ans = invokeContract(server=server, sender=owner, contract=KYC, functionNameSig="addCustomer(string)", functionName="addCustomer", functionArgs=["Naruto"])
    # print(ans.hex())
    print((bytearray.fromhex("86d6520616761696e")).decode("utf-8"))

if __name__ == "__main__":
    main()

# contractAddress -- 0xd49cf73edD179cfc33E7220d158895E2f13fCe51
# abi -- [{'constant': False, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'retrieveName', 'outputs': [{'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'string'}], 'name': 'addCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteContract', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'string'}], 'name': 'retrieveAddress', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'}]

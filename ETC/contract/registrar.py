import sys
sys.path.append("C:\Solc")
sys.path.append("C:\Python_Interpreter\Lib\site-packages")

import json
import requests
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

def main():
    server = Web3(HTTPProvider("https://sokol.poa.network"))
    contractOwnerAddress = generateAddressFromPrivateKey(extractPrivateKey())
    # contractData = generateContract(server, contractOwnerAddress)
    contractData = {'abi': [{'constant': False, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'retrieveName', 'outputs': [{'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'string'}], 'name': 'addCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteContract', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'string'}], 'name': 'retrieveAddress', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'}], 'contractAddress': '0xd49cf73edD179cfc33E7220d158895E2f13fCe51'}
    KYC = server.eth.contract(address=contractData["contractAddress"], abi=contractData["abi"])
    tx = {
        "nonce": server.eth.getTransactionCount(contractOwnerAddress),
        "gasPrice": getGasPrice(speed="fast"),
        "from": "0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69",
        "to": "0xd49cf73edD179cfc33E7220d158895E2f13fCe51",
        "value": 0,
        "gas": 100000,
    }
    signedTX = server.eth.account.signTransaction(
        tx,
        extractPrivateKey()
    )
    check = KYC.functions.addCustomer("Naruto").transact(tx)
    print(check)
    # how to transact()?
if __name__ == "__main__":
    main()

# contractAddress -- 0xd49cf73edD179cfc33E7220d158895E2f13fCe51
# abi -- [{'constant': False, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'retrieveName', 'outputs': [{'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'string'}], 'name': 'addCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteContract', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'string'}], 'name': 'retrieveAddress', 'outputs': [{'name': '', 'type': 'address'}], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'}]

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
    soliditySource = '''
    pragma solidity ^0.5.3;

    contract Mortal {
        address payable owner;

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
    ''' % (contractOwnerAddress, contractOwnerAddress)
    compiledSource = compile_source(soliditySource)
    contractInterface = compiledSource["<stdin>:KYC"]
    rawKYC = server.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
    registTxHash = KYC.constructor().transact()
    txReceipt = server.eth.waitForTransactionReceipt(registTxHash)
    KYC = server.eth.contract(
        address=txReceipt.contractAddress,
        abi = contractInterface['abi']
    )
    return KYC

def main():
    server = Web3(HTTPProvider("https://sokol.poa.network"))
    contract = generateContract()
    contract.functions.addCustomer("Ruslan").call()
    print("Name:")
    userAddress = generateAddressFromPrivateKey(extractPrivateKey())
    response = contract.functions.retrieveName(userAddress).call()
    print(response)

if __name__ == "__main__":
    main()

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
    pragma solidity ^5.0.1;

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

    contract KYC is mortal {

        event Register(indexed address customerAddress, indexed string customerName)
        mapping (address => string) public addressToCustomerName;
        mapping (string => address) public customerNameToAddress

        function registerCustomer(string customerName) public {
            require(name != '', "Please, enter valid name");
            require(msg.sender != address(0));
            require(addressToCustomerName[msg.sender] == false, "You are already registered")
            require(customerNameToAddress[customerName] == false)
            addressToCustomerName[msg.sender] = customerName;
            customerNameToAddress[customerName] = msg.sender;
            emit Register(msg.sender, customerName);
        }

        function deleteCustomer(address customerAddressToDelete) public {
            require(msg.sender == customerAddressToDelete);
            // Delete from DBs
        }

        // Add some mortality
        function deleteContract() public ownerOnly {
            selfdestruct(owner);
        }
    }
    ''' % (contractOwnerAddress, contractOwnerAddress)
    compiledSource = compile_source(source)
    contractInterface = compiledSource["<stdin>:KYC"]
    Contract = server.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
    print("contractInterface:")
    print(contractInterface)

server = Web3(HTTPProvider("https://sokol.poa.network"))
generateContract()

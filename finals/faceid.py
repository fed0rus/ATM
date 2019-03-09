#!/usr/bin/env python

import web3
from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse
from subprocess import check_output
import re
from eth_account import Account
import cv2
import numpy as np
import os
# import dlib
from random import randrange

# Essentials

def setArgs():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--find',
        type=str,
    )
    parser.add_argument(
        '--actions',
        action='store_true',
    )
    parser.add_argument("--add", action="store", nargs='+', help="Send a request for registration")
    parser.add_argument("--balance", action="store", help="Get the balance of your account")
    parser.add_argument("--del", action="store", help="Delete a request for registration")
    parser.add_argument("--cancel", action="store", help="Cancel any request")
    parser.add_argument("--send", action="store", nargs='+', help="Send money by a phone number")
    args = parser.parse_args()
    return vars(args)

# ---------RUS START---------

class User(object):

    def __init__(self, UUID, PIN):
        self.UUID = "0x" + str(UUID.replace('-', ''))
        self.PIN = [int(k) for k in PIN]

    def setServer(self, server):
        self.server = server

    def generatePrivateKey(self):
        UUID = self.UUID
        PIN = self.PIN
        privateKey = server.solidityKeccak(["bytes16"], [b''])
        for k in range(4):
            privateKey = Web3.solidityKeccak(["bytes16", "bytes16", "int8"], [privateKey, UUID, PIN[k]]) # ABI-packed, keccak256 hashed
        self.privateKey = privateKey

    def generateAddress(self):
        account = Account.privateKeyToAccount(self.privateKey)
        self.address = account.address

def scaleValue(value):
    if value == 0:
        return "0 poa"
    elif value < 1e3:
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

def getUser(server, privateKey):
    return server.eth.account.privateKeyToAccount(privateKey)

def getUUID():
    try:
        with open("person.json", 'r') as person:
            return str(json.load(person)["id"])
    except:
        return -1


def getGasPrice(speed):
    try:
        response = requests.get(_gasPriceURL)
        return int((response.json())[speed] * 1e9)
    except:
        return int(_defaultGasPrice)

def cleanTxResponse(rawReceipt):
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

def kycData():
    # with open("KYC.bin", 'r') as bin:
    #     _bytecode = bin.read()
    # with open("KYC.abi", 'r') as abi:
    #     _abi = json.loads(abi.read())
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a03191633179055610d798061003e6000396000f3fe608060405260043610610105576000357c01000000000000000000000000000000000000000000000000000000009004806383904f8d116100a75780639c8e149e116100765780639c8e149e146103755780639ee1bd0f1461038a578063a6f9dae11461039f578063f82c50f1146103d257610105565b806383904f8d146102e5578063851b16f5146102fa578063942ea4661461030f578063987fa1ed1461034257610105565b80634157272a116100e35780634157272a146101c55780634ca1fad8146102735780635a58cd4c1461029d57806374adad1d146102b257610105565b806309e6707d146101075780631d25899b1461014c57806330ccebb514610192575b005b34801561011357600080fd5b5061013a6004803603602081101561012a57600080fd5b5035600160a060020a03166103fc565b60408051918252519081900360200190f35b34801561015857600080fd5b506101766004803603602081101561016f57600080fd5b503561040e565b60408051600160a060020a039092168252519081900360200190f35b34801561019e57600080fd5b5061013a600480360360208110156101b557600080fd5b5035600160a060020a0316610429565b3480156101d157600080fd5b506101da610444565b604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b8381101561021e578181015183820152602001610206565b50505050905001838103825284818151815260200191508051906020019060200280838360005b8381101561025d578181015183820152602001610245565b5050505090500194505050505060405180910390f35b34801561027f57600080fd5b506101056004803603602081101561029657600080fd5b50356104d8565b3480156102a957600080fd5b506101056105ba565b3480156102be57600080fd5b5061013a600480360360208110156102d557600080fd5b5035600160a060020a03166105df565b3480156102f157600080fd5b506101056105f1565b34801561030657600080fd5b506101056106af565b34801561031b57600080fd5b5061013a6004803603602081101561033257600080fd5b5035600160a060020a0316610874565b34801561034e57600080fd5b506101056004803603602081101561036557600080fd5b5035600160a060020a031661088f565b34801561038157600080fd5b506101da610bcd565b34801561039657600080fd5b50610176610c38565b3480156103ab57600080fd5b50610105600480360360208110156103c257600080fd5b5035600160a060020a0316610c48565b3480156103de57600080fd5b50610176600480360360208110156103f557600080fd5b5035610c9c565b60016020526000908152604090205481565b600260205260009081526040902054600160a060020a031681565b600160a060020a031660009081526004602052604090205490565b6003546060908190818060005b838110156104cd5760016004600060038481548110151561046e57fe5b6000918252602080832090910154600160a060020a0316835282019290925260400190205411156104c55760038054829081106104a757fe5b6000918252602090912001548351600160a060020a03909116908490fe5b600101610451565b509093509150509091565b3315156104e457600080fd5b6402540be40081101580156104fe575064174876e7ff8111155b151561050957600080fd5b336000908152600460205260409020541561052357600080fd5b336000908152600160205260409020541561053d57600080fd5b33600081815260046020526040808220849055517fdc79fc57451962cfe3916e686997a49229af75ce2055deb4c0f0fdf3d5d2e7c19190a250600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b600054600160a060020a031633146105d157600080fd5b600054600160a060020a0316ff5b60046020526000908152604090205481565b3315156105fd57600080fd5b336000908152600460205260409020541561061757600080fd5b33600090815260016020526040902054151561063257600080fd5b3360008181526004602052604080822060019055517f64ed2364f9ee0643b60aeffba4ace8805648fad0d546c5efd449d1de10c8dcee9190a2600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b3315156106bb57600080fd5b3360009081526004602052604090205415156106d657600080fd5b33600090815260046020526040812054600114156106f2575060015b3360009081526004602052604081205580156107385760405133907f8c08d387d1333f3da7e980dd7fc958615d513ca73155b6dd2a5a13e17acd116290600090a2610764565b60405133907fffdf549003cf56ac2e863a28d8d5191467cf2a6d5e659f6a649e855a3d8cd8d090600090a25b60035460606000805b8381101561085957600380543391908390811061078657fe5b600091825260209091200154600160a060020a031614156107aa5760019150610851565b8115156108015760038054829081106107bf57fe5b6000918252602090912001548351600160a060020a03909116908490839081106107e557fe5b600160a060020a03909216602092830290910190910152610851565b600380548290811061080f57fe5b6000918252602090912001548351600160a060020a03909116908490600019840190811061083957fe5b600160a060020a039092166020928302909101909101525b60010161076d565b50815161086d906003906020850190610cc4565b5050505050565b600160a060020a031660009081526001602052604090205490565b600054600160a060020a031633146108a657600080fd5b600160a060020a0381166000908152600460205260409020546001811415610a4057600160a060020a038216600081815260016020908152604080832080549084905580845260029092528083208054600160a060020a0319169055519092917f6381abe854c1429e636a1aa796dd6057d1f1e4836874fbb184650908c49804cc91a260035460606000805b83811015610a225786600160a060020a031660038281548110151561095357fe5b600091825260209091200154600160a060020a0316141561097357600191505b8115156109ca57600380548290811061098857fe5b6000918252602090912001548351600160a060020a03909116908490839081106109ae57fe5b600160a060020a03909216602092830290910190910152610a1a565b60038054829081106109d857fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610a0257fe5b600160a060020a039092166020928302909101909101525b600101610932565b508151610a36906003906020850190610cc4565b5050505050610bc9565b6001811115610bc457600160a060020a03821660008181526004602090815260408083205460018352818420819055835260029091528082208054600160a060020a03191684179055517fa010ae0edd95ff06bc66e3eacf9d4f39b23da7ae3056a38dd6c1dcd05630a6da9190a260035460606000805b83811015610ba75785600160a060020a0316600382815481101515610ad857fe5b600091825260209091200154600160a060020a03161415610af857600191505b811515610b4f576003805482908110610b0d57fe5b6000918252602090912001548351600160a060020a0390911690849083908110610b3357fe5b600160a060020a03909216602092830290910190910152610b9f565b6003805482908110610b5d57fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610b8757fe5b600160a060020a039092166020928302909101909101525b600101610ab7565b508151610bbb906003906020850190610cc4565b50505050610bc9565b600080fd5b5050565b6003546060908190818060005b838110156104cd5760046000600383815481101515610bf557fe5b6000918252602080832090910154600160a060020a0316835282019290925260400190205460011415610c305760038054829081106104a757fe5b600101610bda565b600054600160a060020a03165b90565b600054600160a060020a03163314610c5f57600080fd5b600054600160a060020a0382811691161415610c7a57600080fd5b60008054600160a060020a031916600160a060020a0392909216919091179055565b6003805482908110610caa57fe5b600091825260209091200154600160a060020a0316905081565b828054828255906000526020600020908101928215610d19579160200282015b82811115610d195782518254600160a060020a031916600160a060020a03909116178255602090920191600190910190610ce4565b50610d25929150610d29565b5090565b610c4591905b80821115610d25578054600160a060020a0319168155600101610d2f56fea165627a7a723058202e52f7bc564e1e83adeafb45cac989db43f75ddc277a0dc40482640ddd882dc70029"
    _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getStatus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"listAdd","outputs":[{"name":"","type":"address[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_phoneNumber","type":"uint256"}],"name":"addRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"requests","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"cancelRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getNumber","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"applicant","type":"address"}],"name":"confirmRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"listDel","outputs":[{"name":"","type":"address[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"log","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationConfirmed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationConfirmed","type":"event"}]')
    return _bytecode, _abi

def phData():
    # with open("PaymentHandler.bin", 'r') as bin:
    #     _bytecode = bin.read()
    # with open("PaymentHandler.abi", 'r') as abi:
    #     _abi = json.loads(abi.read())
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561018c8061003e6000396000f3fe608060405260043610610050577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c81146100525780639ee1bd0f14610067578063a6f9dae114610098575b005b34801561005e57600080fd5b506100506100cb565b34801561007357600080fd5b5061007c6100f0565b60408051600160a060020a039092168252519081900360200190f35b3480156100a457600080fd5b50610050600480360360208110156100bb57600080fd5b5035600160a060020a03166100ff565b600054600160a060020a031633146100e257600080fd5b600054600160a060020a0316ff5b600054600160a060020a031690565b600054600160a060020a0316331461011657600080fd5b600054600160a060020a038281169116141561013157600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039290921691909117905556fea165627a7a72305820526f825b0f9f8428b7535543052e096311f15a10c1a7ae2ddf550741af04d4df0029"
    _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    return _bytecode, _abi

def checkContract(server, contract):
    ownerAddress = callContract(contract, methodName="whoIsOwner")
    bytecode, abi = kycData()
    source = '''
    pragma solidity >=0.5.0 <0.6.0;

    contract KYC {

        address payable owner;

        constructor() public {
            require(%s != address(0));
            owner = %s;
        }

        event RegistrationRequest(address indexed sender);
        event UnregistrationRequest(address indexed sender);

        event RegistrationCanceled(address indexed sender);
        event UnregistrationCanceled(address indexed sender);

        event RegistrationConfirmed(address indexed sender);
        event UnregistrationConfirmed(address indexed sender);

        mapping (address => uint) public AtN;
        mapping (uint => address) public NtA;

        address[] public log;

        mapping (address => uint) public requests;

        /*
            Status codes:
            == 0:
                no requests
            == 1:
                delete request
            > 1:
                add request (status is number)
        */

        function whoIsOwner() external view returns (address) {
            return owner;
        }

        function changeOwner(address payable newOwner) public {
            require(msg.sender == owner);
            require(newOwner != owner);
            owner = newOwner;
        }

        function getStatus(address _address) external view returns (uint) {
            return requests[_address];
        }

        function getNumber(address _address) external view returns (uint) {
            return AtN[_address];
        }

        function addRequest(uint _phoneNumber) public {
            /* For --del testing */
            /* AtN[0x84F89561c38b380e97aed3F6f8f28263C60925F2] = _phoneNumber; */
            require(msg.sender != address(0));
            require(_phoneNumber >= 10000000000 && _phoneNumber <= 99999999999);
            require(requests[msg.sender] == 0);
            require(AtN[msg.sender] == 0);
            requests[msg.sender] = _phoneNumber;
            emit RegistrationRequest(msg.sender);
            log.push(msg.sender);
        }

        function delRequest() public {
            require(msg.sender != address(0));
            require(requests[msg.sender] == 0);
            require(AtN[msg.sender] != 0);
            requests[msg.sender] = 1;
            emit UnregistrationRequest(msg.sender);
            log.push(msg.sender);
        }

        function cancelRequest() public {
            require(msg.sender != address(0));
            require(requests[msg.sender] != 0);
            bool mutex = false;
            if (requests[msg.sender] == 1) {
                mutex = true;
            }
            requests[msg.sender] = 0;
            if (mutex) {
                emit UnregistrationCanceled(msg.sender);
            }
            else {
                emit RegistrationCanceled(msg.sender);
            }
            uint l = log.length;
            address[] memory save;
            bool flag = false;
            for (uint i = 0; i < l; ++i) {
                if (log[i] == msg.sender) {
                    flag = true;
                }
                else {
                    if (!flag) {
                        save[i] = log[i];
                    }
                    else {
                        save[i - 1] = log[i];
                    }
                }
            }
            log = save;
        }

        function listAdd() external view returns (address[] memory, uint[] memory) {
            uint l = log.length;
            address[] memory retA;
            uint[] memory retN;
            for (uint i = 0; i < l; ++i) {
                if (requests[log[i]] > 1) {
                    retA[retA.length] = log[i];
                    retN[retN.length] = requests[log[i]];
                }
            }
            return (retA, retN);
        }

        function listDel() external view returns (address[] memory, uint[] memory) {
            uint l = log.length;
            address[] memory retA;
            uint[] memory retN;
            for (uint i = 0; i < l; ++i) {
                if (requests[log[i]] == 1) {
                    retA[retA.length] = log[i];
                    retN[retN.length] = AtN[log[i]];
                }
            }
            return (retA, retN);
        }

        function confirmRequest(address applicant) public {
            require(msg.sender == owner);
            uint status = requests[applicant];
            if (status == 1) {
                uint number = AtN[applicant];
                AtN[applicant] = 0;
                NtA[number] = address(0);
                emit UnregistrationConfirmed(applicant);

                uint l = log.length;
                address[] memory save;
                bool flag = false;
                for (uint i = 0; i < l; ++i) {
                    if (log[i] == applicant) {
                        flag = true;
                    }
                    if (!flag) {
                        save[i] = log[i];
                    }
                    else {
                        save[i - 1] = log[i];
                    }
                }
                log = save;
            }
            else if (status > 1) {
                AtN[applicant] = requests[applicant];
                NtA[requests[applicant]] = applicant;
                emit RegistrationConfirmed(applicant);

                uint l = log.length;
                address[] memory save;
                bool flag = false;
                for (uint i = 0; i < l; ++i) {
                    if (log[i] == applicant) {
                        flag = true;
                    }
                    if (!flag) {
                        save[i] = log[i];
                    }
                    else {
                        save[i - 1] = log[i];
                    }
                }
                log = save;
            }
            else {
                revert();
            }
        }

        function () external payable {}

        function deleteContract() external {
            require(msg.sender == owner);
            selfdestruct(owner);
        }
    }''' % (ownerAddress, ownerAddress)
    with open("checkContract.sol", 'w') as file:
        file.write(source)
    compiled_registrar = check_output(["solc", "--abi", "--bin", "--optimize", "-o", "./", "checkContract.sol"]).decode()
    start = compiled_registrar.find("Binary:")
    end = compiled_registrar.find("Contract JSON ABI")
    suspicion = compiled_registrar[start + 11:end - 4]
    suspicion = server.eth.getCode(contract.address).hex()[2:]
    print(bytecode)
    print("-------------------")
    print(suspicion)
    # return bytecode == suspicion
    return True


def send(server, sender, dest, val):
    txUnsigned = {
        "from": sender.address,
        "to": dest,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gas": 21000,
        "gasPrice": getGasPrice(speed="fast"),
        "value": int(val),
    }
    txSigned = sender.signTransaction(txUnsigned)
    try:
        txHash = server.eth.sendRawTransaction(txSigned.rawTransaction).hex()
    except:
        return "No funds to send the payment"
    return txHash

def getContract(server, flag):

    try:
        with open("registrar.json", 'r') as db:
            data = json.load(db)
    except:
        return "No contract address"
    # switch contract type
    if flag == "kyc":
        _stub, _abi = kycData()
    elif flag == "ph":
        _stub, _abi = phData()
    contractAddress = data["registrar"]["address"]
    _contract = server.eth.contract(address=contractAddress, abi=_abi)
    return _contract

def invokeContract(server, sender, contract, methodName, methodArgs):

    _args = str(methodArgs)[1:-1]
    invoker = "contract.functions.{methodName}({methodArgs})".format(
        methodName=methodName,
        methodArgs=_args,
    )
    _gas = eval(invoker).estimateGas({"from": sender.address})
    txUnsigned = eval(invoker).buildTransaction({
        "from": sender.address,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gas": _gas,
        "gasPrice": getGasPrice(speed="fast"),
    })
    txSigned = sender.signTransaction(txUnsigned)
    txHash = server.eth.sendRawTransaction(txSigned.rawTransaction).hex()
    return txHash

def callContract(contract, methodName, methodArgs=""):

    _args = str(methodArgs)[1:-1]
    response = "contract.functions.{methodName}({methodArgs}).call()".format(
    methodName=methodName,
    methodArgs=_args,
    )
    return eval(response)

# ---------------------------

def addRequest(server, user, phoneNumber):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    _user = getUser(server, user.privateKey)

    if server.eth.getBalance(_user.address) <= 0:
        return "No funds to send the request"

    if checkContract(server, _contract):
        status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
        if status == 0:
            txHash = invokeContract(server, _user, _contract, methodName="addRequest", methodArgs=[phoneNumber])
            return "Registration request sent by {}".format(txHash)
        elif status > 1:
            return "Registration request already sent"
        elif status == 1:
            return "Unregistration request already sent. SWW"
    else:
        return "Seems that the contract address is not the registrar contract"

def delRequest(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    _user = getUser(server, user.privateKey)

    if server.eth.getBalance(_user.address) <= 0:
        return "No funds to send the request"

    if (checkContract(server, _contract)):
        status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
        registeredNumber = callContract(_contract, methodName="getNumber", methodArgs=[user.address])
        if registeredNumber == 0:
            return "Account is not registered yet"
        else:
            if status == 1:
                return "Unregistration request already sent"
            elif status > 1:
                return "Conflict: registration request already sent"
            elif status == 0:
                txHash = invokeContract(server, _user, _contract, methodName="delRequest", methodArgs=[])
                return "Unregistration request sent by {}".format(txHash)
    else:
        return "Seems that the contract address is not the registrar contract"

def cancelRequest(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    _user = getUser(server, user.privateKey)

    if server.eth.getBalance(user.address) <= 0:
        return "No funds to send the request"
    if (checkContract(server, _contract)):
        status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
        if status == 0:
            return "No requests found"

        elif status == 1:
            txHash = invokeContract(server, _user, _contract, methodName="cancelRequest", methodArgs=[])
            return "Unregistration canceled by {}".format(txHash)

        elif status > 1:
            txHash = invokeContract(server, _user, _contract, methodName="cancelRequest", methodArgs=[])
            return "Registration canceled by {}".format(txHash)
    else:
        return "Seems that the contract address is not the registrar contract"

# def sendByNumber(server, user, pn, val):
#     _contract = getContract(server, flag="kyc")
#     if _contract == "No contract address":
#         return _contract
#     if not isContract(_contract):
#         return "Seems that the contract address is not the registrar contract"
#     _user = getUser(server, user.privateKey)
#     refinedNumber = int(str(pn)[1:])
#     destAddress = invokeContract(server, _user, _contract, methodName="getAddressByNumber", methodArgs=[refinedNumber])
#     if destAddress == 0:
#         print("No account with the phone number {}".format(pn))
#     elif (server.isAddress(destAddress)):
#         txHash = send(server, _user, destAddress, val)
#         if txHash == "No funds to send the payment":
#             print(txHash)
#         print("Payment of {a} to {d} scheduled".format(a=scaleValue(int(val)), d=pn))
#         print("Transaction Hash: {}".format(txHash))
#     else:
#         raise ValueError

# ----------RUS END----------

# ---------MAG START---------


def GetKey():
    with open('faceapi.json') as f:
        privateKey = eval(f.read())['key']
    return privateKey

def GetGroupId():
    with open('faceapi.json') as f:
        groupId = eval(f.read())['groupId']
    return groupId

def GetBaseUrl():
    with open('faceapi.json') as f:
        serviceUrl = eval(f.read())['serviceUrl']
    return serviceUrl

def MakeDetectRequest(buf):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'returnFaceId': True,
        'returnFaceRectangle': False,
    }
    baseUrl = GetBaseUrl() + 'detect/'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
        data=buf,
    )
    return req.json()

def GetOctetStream(image):
    ret, buf = cv2.imencode('.jpg', image)
    return buf.tobytes()

def Detect(videoFrames):
    result = []
    for frame in videoFrames:
        image = GetOctetStream(frame)
        req = MakeDetectRequest(image)
        if (len(req) != 0):
            result.append(req[0]['faceId'])
    return result

def Identify(videoFrames):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    ids = Detect(videoFrames)
    data = {
        'faceIds': ids,
        'personGroupId': GetGroupId(),
    }
    baseUrl = GetBaseUrl() + '/identify'
    req = requests.post(
        baseUrl,
        headers=headers,
        json=data,
    )
    return req.json()

def GetVideoFrames(videoName):
    vcap = cv2.VideoCapture(videoName)
    result = []
    frames = []
    while (True):
        ret, frame = vcap.read()
        if (frame is None):
            break
        else:
            frames.append(frame)
    if (len(frames) < 5):
        return result
    for i in range(0, len(frames), len(frames) // 4):
        if (len(result) == 4 or len(frames) < 5):
            break
        result.append(frames[i])
    result.append(frames[-1])
    vcap.release()
    return result

def GetTrainingStatus():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId': GetGroupId(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/training'
    req = requests.get(
        baseUrl,
        params=params,
        headers=headers,
    )
    return req.json()

def GetList():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons'
    req = requests.get(
        baseUrl,
        headers=headers,
    )
    return req

def CreateFile(id):
    f = open('person.json', 'w')
    f.write('{"id": "' + id + '"}')
    f.close()

def DeleteFile():
    if (os.path.isfile('person.json')):
        os.remove('person.json')

def GetPersonsData():
    req = GetList()
    if (str(req) == '<Response [200]>'):
        req = GetList().json()
        persons = []
        for person in req:
            persons.append({
                'personId':person['personId'],
                'name':person['name'],
                'userData':person['userData']
            })
        return persons
    else:
        return 'The group does not exist'

def Find(videoName):
    videoFrames = GetVideoFrames(videoName)
    persons = GetPersonsData()
    if (len(videoFrames) < 5):
        print('The video does not follow requirements')
        DeleteFile()
        return None
    if (persons == 'The group does not exist'):
        print('The service is not ready')
        DeleteFile()
        return None
    f = 1
    for person in persons:
        if (person['userData'] != 'trained'):
            f = 0
    if (f == 0):
        print('The service is not ready')
        DeleteFile()
        return None
    else:
        result = Identify(videoFrames)
        if (len(result) < 5):
            print('The video does not follow requirements')
            DeleteFile()
            return None
        candidates = dict()
        for frame in result:
            for candidate in frame['candidates']:
                currPersonId = candidate['personId']
                currConfidence = candidate['confidence']
                if (candidates.get(currPersonId) == None):
                    if (currConfidence >= 0.5):
                        candidates[currPersonId] = currConfidence
                else:
                    if (currConfidence >= 0.5):
                        candidates[currPersonId] += currConfidence
                    else:
                        candidates[currPersonId] = -100000
        if (len(candidates) == 0):
            print('The person was not found')
            DeleteFile()
            return None
        maxConfidence = 0
        bestCandidate = ''
        for candidate, confidence in candidates.items():
            if (confidence >= 2.5):
                if (maxConfidence < confidence):
                    bestCandidate = candidate
                    maxConfidence = confidence
        if (maxConfidence < 2.5):
            print('The person was not found')
            DeleteFile()
            return None
        else:
            print(bestCandidate + ' identified')
            CreateFile(bestCandidate)
            return None

def SetActions():
    f = open('actions.json', 'w')
    actions = [
        'yaw right',
        'yaw left',
        'roll right',
        'roll left',
        'close right eye',
        'close left eye',
        'open mouth',
    ]
    ans = ''
    for i in range(7):
        rand = randrange(len(actions))
        ans += actions[rand] + '\n'
        actions.remove(actions[rand])
    f.write(ans)
    f.close()

# ----------MAG END-----------

# ---------MAIN MUTEX---------

if __name__ == "__main__":

    # ----------START SET------------

    with open("network.json", 'r') as ethConfig:
        global _defaultGasPrice
        global _gasPriceURL
        global _rpcURL
        read = json.load(ethConfig)
        _rpcURL = str(read["rpcUrl"])
        _gasPriceURL = str(read["gasPriceUrl"])
        _defaultGasPrice = str(read["defaultGasPrice"])

    args = setArgs()
    server = Web3(HTTPProvider(_rpcURL))

    # -----------END SET-------------

    # ------ACCEPTANCE ZONE START----

    if args["balance"] is not None:
        getBalanceByID(server)

    elif args["add"] is not None:

        _UUID = getUUID()
        if _UUID == -1:
            print("ID is not found")
        else:
            _phoneNumber = args["add"][1]
            if _phoneNumber[0] == '+' and _phoneNumber[1:].isdigit() and len(_phoneNumber) == 12:
                _PIN = args["add"][0]
                user = User(_UUID, _PIN)
                user.generatePrivateKey()
                user.generateAddress()
                print(addRequest(server, user, int(_phoneNumber[1:])))
            else:
                print("Incorrect phone number")

    elif args["del"] is not None:

        _UUID = getUUID()
        if _UUID == -1:
            print("ID is not found")
        else:
            _PIN = args["del"]
            user = User(_UUID, _PIN)
            user.generatePrivateKey()
            user.generateAddress()
            print(delRequest(server, user))

    # ------ACCEPTANCE ZONE END------

    # -------DANGER ZONE START-------
    # US-016
    elif args["cancel"] is not None:

            _UUID = getUUID()
            if _UUID == -1:
                print("ID is not found")
            else:
                _PIN = args["cancel"]
                user = User(_UUID, _PIN)
                user.generatePrivateKey()
                user.generateAddress()
                print(cancelRequest(server, user))

    # US-017
    # elif args["send"] is not None:
    #     try:
    #         with open("person.json", 'r') as person:
    #             _UUID = str(json.load(person)["id"])
    #         _PIN = args["send"][0]
    #         _phoneNumber = args["send"][1]
    #         if len(str(_phoneNumber)) != 11:
    #             print("Incorrect phone number")
    #         else:
    #             _value = args["send"][2]
    #             user = User(_UUID, _PIN)
    #             user.generatePrivateKey()
    #             user.generateAddress()
    #             sendByNumber(server, user, _phoneNumber, _value)
    #     except:
    #         print("ID is not found")

    # --------DANGER ZONE END--------

    elif (args['find'] != None):
        Find(args['find'])

    elif (args['actions'] == True):
        SetActions()

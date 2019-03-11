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
    parser.add_argument("--ops", action="store", help="List the payments history")
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
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561101e8061003e6000396000f3fe60806040526004361061011b576000357c010000000000000000000000000000000000000000000000000000000090048063942ea466116100b2578063b93f9b0a11610081578063b93f9b0a14610325578063bd4782431461034f578063f82c50f11461037f578063fc735e99146103a9578063fddc5f28146103d25761011b565b8063942ea46614610277578063987fa1ed146102aa5780639ee1bd0f146102dd578063a6f9dae1146102f25761011b565b80635a58cd4c116100ee5780635a58cd4c1461020557806374adad1d1461021a57806383904f8d1461024d578063851b16f5146102625761011b565b806309e6707d1461011d5780631d25899b1461016257806330ccebb5146101a85780634ca1fad8146101db575b005b34801561012957600080fd5b506101506004803603602081101561014057600080fd5b5035600160a060020a0316610528565b60408051918252519081900360200190f35b34801561016e57600080fd5b5061018c6004803603602081101561018557600080fd5b503561053a565b60408051600160a060020a039092168252519081900360200190f35b3480156101b457600080fd5b50610150600480360360208110156101cb57600080fd5b5035600160a060020a0316610555565b3480156101e757600080fd5b5061011b600480360360208110156101fe57600080fd5b5035610574565b34801561021157600080fd5b5061011b610656565b34801561022657600080fd5b506101506004803603602081101561023d57600080fd5b5035600160a060020a031661067b565b34801561025957600080fd5b5061011b61068d565b34801561026e57600080fd5b5061011b61074b565b34801561028357600080fd5b506101506004803603602081101561029a57600080fd5b5035600160a060020a0316610910565b3480156102b657600080fd5b5061011b600480360360208110156102cd57600080fd5b5035600160a060020a0316610953565b3480156102e957600080fd5b5061018c610ca8565b3480156102fe57600080fd5b5061011b6004803603602081101561031557600080fd5b5035600160a060020a0316610cb8565b34801561033157600080fd5b5061018c6004803603602081101561034857600080fd5b5035610d0c565b34801561035b57600080fd5b5061011b6004803603604081101561037257600080fd5b5080359060200135610d4e565b34801561038b57600080fd5b5061018c600480360360208110156103a257600080fd5b5035610e48565b3480156103b557600080fd5b506103be610e70565b604080519115158252519081900360200190f35b3480156103de57600080fd5b50610405600480360360208110156103f557600080fd5b5035600160a060020a0316610e75565b6040518080602001806020018060200180602001858103855289818151815260200191508051906020019060200280838360005b83811015610451578181015183820152602001610439565b50505050905001858103845288818151815260200191508051906020019060200280838360005b83811015610490578181015183820152602001610478565b50505050905001858103835287818151815260200191508051906020019060200280838360005b838110156104cf5781810151838201526020016104b7565b50505050905001858103825286818151815260200191508051906020019060200280838360005b8381101561050e5781810151838201526020016104f6565b505050509050019850505050505050505060405180910390f35b60016020526000908152604090205481565b600260205260009081526040902054600160a060020a031681565b600160a060020a0381166000908152600460205260409020545b919050565b33151561058057600080fd5b6402540be400811015801561059a575064174876e7ff8111155b15156105a557600080fd5b33600090815260046020526040902054156105bf57600080fd5b33600090815260016020526040902054156105d957600080fd5b33600081815260046020526040808220849055517fdc79fc57451962cfe3916e686997a49229af75ce2055deb4c0f0fdf3d5d2e7c19190a250600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b600054600160a060020a0316331461066d57600080fd5b600054600160a060020a0316ff5b60046020526000908152604090205481565b33151561069957600080fd5b33600090815260046020526040902054156106b357600080fd5b3360009081526001602052604090205415156106ce57600080fd5b3360008181526004602052604080822060019055517f64ed2364f9ee0643b60aeffba4ace8805648fad0d546c5efd449d1de10c8dcee9190a2600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b33151561075757600080fd5b33600090815260046020526040902054151561077257600080fd5b336000908152600460205260408120546001141561078e575060015b3360009081526004602052604081205580156107d45760405133907f8c08d387d1333f3da7e980dd7fc958615d513ca73155b6dd2a5a13e17acd116290600090a2610800565b60405133907fffdf549003cf56ac2e863a28d8d5191467cf2a6d5e659f6a649e855a3d8cd8d090600090a25b60035460606000805b838110156108f557600380543391908390811061082257fe5b600091825260209091200154600160a060020a0316141561084657600191506108ed565b81151561089d57600380548290811061085b57fe5b6000918252602090912001548351600160a060020a039091169084908390811061088157fe5b600160a060020a039092166020928302909101909101526108ed565b60038054829081106108ab57fe5b6000918252602090912001548351600160a060020a0390911690849060001984019081106108d557fe5b600160a060020a039092166020928302909101909101525b600101610809565b508151610909906003906020850190610f37565b5050505050565b600160a060020a03811660009081526001602052604081205415156109375750600061056f565b50600160a060020a031660009081526001602052604090205490565b600054600160a060020a0316331461096a57600080fd5b600160a060020a0381166000908152600460205260409020546001811415610b1557600160a060020a0382166000818152600160209081526040808320805490849055808452600283528184208054600160a060020a03191690558484526004909252808320839055519092917f6381abe854c1429e636a1aa796dd6057d1f1e4836874fbb184650908c49804cc91a260035460606000805b83811015610af75786600160a060020a0316600382815481101515610a2457fe5b600091825260209091200154600160a060020a03161415610a485760019150610aef565b811515610a9f576003805482908110610a5d57fe5b6000918252602090912001548351600160a060020a0390911690849083908110610a8357fe5b600160a060020a03909216602092830290910190910152610aef565b6003805482908110610aad57fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610ad757fe5b600160a060020a039092166020928302909101909101525b600101610a03565b508151610b0b906003906020850190610f37565b5050505050610ca4565b6001811115610ca457600160a060020a03821660008181526004602081815260408084208054600184528286208190558552600283528185208054600160a060020a031916871790558585529290915290829055517fa010ae0edd95ff06bc66e3eacf9d4f39b23da7ae3056a38dd6c1dcd05630a6da9190a260035460606000805b83811015610c8b5785600160a060020a0316600382815481101515610bb857fe5b600091825260209091200154600160a060020a03161415610bdc5760019150610c83565b811515610c33576003805482908110610bf157fe5b6000918252602090912001548351600160a060020a0390911690849083908110610c1757fe5b600160a060020a03909216602092830290910190910152610c83565b6003805482908110610c4157fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610c6b57fe5b600160a060020a039092166020928302909101909101525b600101610b97565b508151610c9f906003906020850190610f37565b505050505b5050565b600054600160a060020a03165b90565b600054600160a060020a03163314610ccf57600080fd5b600054600160a060020a0382811691161415610cea57600080fd5b60008054600160a060020a031916600160a060020a0392909216919091179055565b600081815260026020526040812054600160a060020a03161515610d325750600061056f565b50600090815260026020526040902054600160a060020a031690565b331515610d5a57600080fd5b610d62610f9c565b338152602081019283526040810191825242606082019081526005805460018101825560009190915291517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db060049093029283018054600160a060020a031916600160a060020a0390921691909117905592517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db182015590517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db282015590517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db390910155565b6003805482908110610e5657fe5b600091825260209091200154600160a060020a0316905081565b600190565b600554606090819081908190819081908190819060005b81811015610f26578a600160a060020a0316600582815481101515610ead57fe5b6000918252602090912060049091020154600160a060020a03161415610ed65785516001908790fe5b600160a060020a038b166000908152600160205260409020546005805483908110610efd57fe5b9060005260206000209060040201600101541415610f1e5785516000908790fe5b600101610e8c565b509399929850909650945092505050565b828054828255906000526020600020908101928215610f8c579160200282015b82811115610f8c5782518254600160a060020a031916600160a060020a03909116178255602090920191600190910190610f57565b50610f98929150610fce565b5090565b6080604051908101604052806000600160a060020a031681526020016000815260200160008152602001600081525090565b610cb591905b80821115610f98578054600160a060020a0319168155600101610fd456fea165627a7a7230582031b38a39cb23177069cee5b8bd513962195f496cd0052717afc5848a822d138a0029"
    _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getStatus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_phoneNumber","type":"uint256"}],"name":"addRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"requests","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"cancelRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getNumber","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"applicant","type":"address"}],"name":"confirmRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_pn","type":"uint256"}],"name":"getAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_pn","type":"uint256"},{"name":"_value","type":"uint256"}],"name":"sendMoney","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"log","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"verify","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"caller","type":"address"}],"name":"listPayments","outputs":[{"name":"","type":"bool[]"},{"name":"","type":"uint256[]"},{"name":"","type":"uint256[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationConfirmed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationConfirmed","type":"event"}]')
    return _bytecode, _abi

def phData():
    # with open("PaymentHandler.bin", 'r') as bin:
    #     _bytecode = bin.read()
    # with open("PaymentHandler.abi", 'r') as abi:
    #     _abi = json.loads(abi.read())
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561018c8061003e6000396000f3fe608060405260043610610050577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c81146100525780639ee1bd0f14610067578063a6f9dae114610098575b005b34801561005e57600080fd5b506100506100cb565b34801561007357600080fd5b5061007c6100f0565b60408051600160a060020a039092168252519081900360200190f35b3480156100a457600080fd5b50610050600480360360208110156100bb57600080fd5b5035600160a060020a03166100ff565b600054600160a060020a031633146100e257600080fd5b600054600160a060020a0316ff5b600054600160a060020a031690565b600054600160a060020a0316331461011657600080fd5b600054600160a060020a038281169116141561013157600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039290921691909117905556fea165627a7a72305820526f825b0f9f8428b7535543052e096311f15a10c1a7ae2ddf550741af04d4df0029"
    _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    return _bytecode, _abi

def checkContract(contract, flag):
    try:
        return callContract(contract, methodName="verify", methodArgs=[])
    except:
        return False

def send(server, sender, dest, val):
    sender = getUser(server, sender.privateKey)
    txUnsigned = {
        "from": sender.address,
        "to": dest,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gas": 21000,
        "gasPrice": getGasPrice(speed="fast"),
        "value": val,
    }
    txSigned = sender.signTransaction(txUnsigned)
    txHash = server.eth.sendRawTransaction(txSigned.rawTransaction).hex()
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

def invokeContract(server, sender, contract, methodName, methodArgs, rec=False, ni=0):

    _args = str(methodArgs)[1:-1]
    invoker = "contract.functions.{methodName}({methodArgs})".format(
        methodName=methodName,
        methodArgs=_args,
    )
    try:
        _gas = eval(invoker).estimateGas({"from": sender.address})
        txUnsigned = eval(invoker).buildTransaction({
            "from": sender.address,
            "nonce": server.eth.getTransactionCount(sender.address) + ni,
            "gas": _gas,
            "gasPrice": getGasPrice(speed="fast"),
        })
        txSigned = sender.signTransaction(txUnsigned)
        txHash = server.eth.sendRawTransaction(txSigned.rawTransaction).hex()
        return txHash
    except ValueError:
        if rec:
            _gas = 1000000
            txUnsigned = eval(invoker).buildTransaction({
                "from": sender.address,
                "nonce": server.eth.getTransactionCount(sender.address) + ni,
                "gas": _gas,
                "gasPrice": getGasPrice(speed="fast"),
            })
            txSigned = sender.signTransaction(txUnsigned)
            txHash = server.eth.sendRawTransaction(txSigned.rawTransaction).hex()
            return '-' + txHash

def callContract(contract, methodName, methodArgs=""):

    _args = str(methodArgs)[1:-1]
    response = "contract.functions.{methodName}({methodArgs}).call()".format(
        methodName=methodName,
        methodArgs=_args
    )
    return eval(response)

# ---------------------------

def addRequest(server, user, phoneNumber):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    if not checkContract(_contract, flag="kyc"):
        return "Seems that the contract address is not the registrar contract"

    _user = getUser(server, user.privateKey)

    if server.eth.getBalance(_user.address) <= 0:
        return "No funds to send the request"

    status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
    if status == 0:
        txHash = invokeContract(server, _user, _contract, methodName="addRequest", methodArgs=[phoneNumber])
        return "Registration request sent by {}".format(txHash)
    elif status > 1:
        return "Registration request already sent"
    elif status == 1:
        return "Unregistration request already sent. SWW"

def delRequest(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    if not checkContract(_contract, flag="kyc"):
        return "Seems that the contract address is not the registrar contract"

    _user = getUser(server, user.privateKey)

    if server.eth.getBalance(_user.address) <= 0:
        return "No funds to send the request"

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

def cancelRequest(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    if not checkContract(_contract, flag="kyc"):
        return "Seems that the contract address is not the registrar contract"

    _user = getUser(server, user.privateKey)

    if server.eth.getBalance(user.address) <= 0:
        return "No funds to send the request"

    status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
    if status == 0:
        return "No requests found"

    elif status == 1:
        txHash = invokeContract(server, _user, _contract, methodName="cancelRequest", methodArgs=[])
        return "Unregistration canceled by {}".format(txHash)

    elif status > 1:
        txHash = invokeContract(server, _user, _contract, methodName="cancelRequest", methodArgs=[])
        return "Registration canceled by {}".format(txHash)

def sendByNumber(server, user, pn, val):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    if not checkContract(_contract, flag="kyc"):
        return "Seems that the contract address is not the registrar contract"

    _user = getUser(server, user.privateKey)

    if server.eth.getBalance(user.address) < int(val) + 21000 * getGasPrice(speed="fast"):
        return "No funds to send the payment"

    refinedNumber = int(str(pn)[1:])
    destAddress = callContract(_contract, methodName="getAddress", methodArgs=[refinedNumber])
    if destAddress == "0x0000000000000000000000000000000000000000":
        return "No account with the phone number {}".format(pn)
    else:
        txHash = send(server, _user, destAddress, int(val))
        invokeContract(server, _user, _contract, methodName="sendMoney", methodArgs=[refinedNumber, int(val)], ni=1)
        return "Payment of {a} to {d} scheduled\nTransaction Hash: {t}".format(a=scaleValue(int(val)), d=pn, t=txHash)

def listPayments(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    if not checkContract(_contract, flag="kyc"):
        return "Seems that the contract address is not the registrar contract"

    _user = getUser(server, user.privateKey)

    if server.eth.getBalance(_user.address) <= 0:
        return "No funds to send the request"

    fromTo, numbers, values, times = callContract(_contract, methodName="listPayments", methodArgs=[user.address])

    # for k in len(fromTo):
    #     if fromTo[k]:
    #         time = setTime(times[k])
    #         print("{t} FROM: +{n} {v}".format(t=time, n=numbers[k], v=scaleValue(values[k])))
    #
    #     elif not fromTo[k]:
    #         pass



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
    res = Detect(videoFrames)
    if (len(res) < 5):
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
        'Yaw',
        'Roll',
        'CloseLeftEye',
        'CloseRightEye',
        'OpenMouth',
    ]
    coun = randrange(3, 5)
    finalActions = []
    for i in range(coun):
        a = randrange(len(actions))
        currAction = actions[a]
        actions.remove(currAction)
        if currAction == 'Yaw':
            b = randrange(2)
            if (b == 0):
                currAction = 'YawLeft'
            else:
                currAction = 'YawRight'
        elif currAction == 'Roll':
            b = randrange(2)
            if (b == 0):
                currAction = 'RollLeft'
            else:
                currAction = 'RollRight'
        finalActions.append(currAction)
    di = dict()
    di['actions'] = []
    for action in finalActions:
        di['actions'].append(action)
    f.write(str(di))
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
            if len(args["add"]) == 2:
                _phoneNumber = args["add"][1]
                if _phoneNumber[0] == '+' and _phoneNumber[1:].isdigit() and len(_phoneNumber) == 12:
                    _PIN = args["add"][0]
                    user = User(_UUID, _PIN)
                    user.generatePrivateKey()
                    user.generateAddress()
                    print(addRequest(server, user, int(_phoneNumber[1:])))
                else:
                    print("Incorrect phone number")
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


    elif args["send"] is not None:

        _UUID = getUUID()
        if _UUID == -1:
            print("ID is not found")
        else:
            _PIN = args["send"][0]
            _phoneNumber = args["send"][1]
            if _phoneNumber[0] == '+' and _phoneNumber[1:].isdigit() and len(_phoneNumber) == 12:
                _value = args["send"][2]
                user = User(_UUID, _PIN)
                user.generatePrivateKey()
                user.generateAddress()
                print(sendByNumber(server, user, _phoneNumber, _value))
            else:
                print("Incorrect phone number")

    # ------ACCEPTANCE ZONE END------

    # -------DANGER ZONE START-------

    elif args["ops"] is not None:

        _UUID = getUUID()
        if _UUID == -1:
            print("ID is not found")
        else:
            _PIN = args["send"][0]
            user = User(_UUID, _PIN)
            user.generatePrivateKey()
            user.generateAddress()
            print(listPayments(server, user))

    # --------DANGER ZONE END--------

    elif (args['find'] != None):
        Find(args['find'])

    elif (args['actions'] == True):
        SetActions()

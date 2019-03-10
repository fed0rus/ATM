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
    with open("KYC.bin", 'r') as bin:
        _bytecode = bin.read()
    with open("KYC.abi", 'r') as abi:
        _abi = json.loads(abi.read())
    # _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a03191633179055610de48061003e6000396000f3fe608060405260043610610110576000357c010000000000000000000000000000000000000000000000000000000090048063942ea466116100a7578063b93f9b0a11610076578063b93f9b0a1461031a578063bd47824314610344578063f82c50f114610374578063fc735e991461039e57610110565b8063942ea4661461026c578063987fa1ed1461029f5780639ee1bd0f146102d2578063a6f9dae1146102e757610110565b80635a58cd4c116100e35780635a58cd4c146101fa57806374adad1d1461020f57806383904f8d14610242578063851b16f51461025757610110565b806309e6707d146101125780631d25899b1461015757806330ccebb51461019d5780634ca1fad8146101d0575b005b34801561011e57600080fd5b506101456004803603602081101561013557600080fd5b5035600160a060020a03166103c7565b60408051918252519081900360200190f35b34801561016357600080fd5b506101816004803603602081101561017a57600080fd5b50356103d9565b60408051600160a060020a039092168252519081900360200190f35b3480156101a957600080fd5b50610145600480360360208110156101c057600080fd5b5035600160a060020a03166103f4565b3480156101dc57600080fd5b50610110600480360360208110156101f357600080fd5b5035610413565b34801561020657600080fd5b506101106104f5565b34801561021b57600080fd5b506101456004803603602081101561023257600080fd5b5035600160a060020a031661051a565b34801561024e57600080fd5b5061011061052c565b34801561026357600080fd5b506101106105ea565b34801561027857600080fd5b506101456004803603602081101561028f57600080fd5b5035600160a060020a03166107af565b3480156102ab57600080fd5b50610110600480360360208110156102c257600080fd5b5035600160a060020a03166107f2565b3480156102de57600080fd5b50610181610b30565b3480156102f357600080fd5b506101106004803603602081101561030a57600080fd5b5035600160a060020a0316610b40565b34801561032657600080fd5b506101816004803603602081101561033d57600080fd5b5035610b94565b34801561035057600080fd5b506101106004803603604081101561036757600080fd5b5080359060200135610bd6565b34801561038057600080fd5b506101816004803603602081101561039757600080fd5b5035610cd0565b3480156103aa57600080fd5b506103b3610cf8565b604080519115158252519081900360200190f35b60016020526000908152604090205481565b600260205260009081526040902054600160a060020a031681565b600160a060020a0381166000908152600460205260409020545b919050565b33151561041f57600080fd5b6402540be4008110158015610439575064174876e7ff8111155b151561044457600080fd5b336000908152600460205260409020541561045e57600080fd5b336000908152600160205260409020541561047857600080fd5b33600081815260046020526040808220849055517fdc79fc57451962cfe3916e686997a49229af75ce2055deb4c0f0fdf3d5d2e7c19190a250600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b600054600160a060020a0316331461050c57600080fd5b600054600160a060020a0316ff5b60046020526000908152604090205481565b33151561053857600080fd5b336000908152600460205260409020541561055257600080fd5b33600090815260016020526040902054151561056d57600080fd5b3360008181526004602052604080822060019055517f64ed2364f9ee0643b60aeffba4ace8805648fad0d546c5efd449d1de10c8dcee9190a2600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b3315156105f657600080fd5b33600090815260046020526040902054151561061157600080fd5b336000908152600460205260408120546001141561062d575060015b3360009081526004602052604081205580156106735760405133907f8c08d387d1333f3da7e980dd7fc958615d513ca73155b6dd2a5a13e17acd116290600090a261069f565b60405133907fffdf549003cf56ac2e863a28d8d5191467cf2a6d5e659f6a649e855a3d8cd8d090600090a25b60035460606000805b838110156107945760038054339190839081106106c157fe5b600091825260209091200154600160a060020a031614156106e5576001915061078c565b81151561073c5760038054829081106106fa57fe5b6000918252602090912001548351600160a060020a039091169084908390811061072057fe5b600160a060020a0390921660209283029091019091015261078c565b600380548290811061074a57fe5b6000918252602090912001548351600160a060020a03909116908490600019840190811061077457fe5b600160a060020a039092166020928302909101909101525b6001016106a8565b5081516107a8906003906020850190610cfd565b5050505050565b600160a060020a03811660009081526001602052604081205415156107d65750600061040e565b50600160a060020a031660009081526001602052604090205490565b600054600160a060020a0316331461080957600080fd5b600160a060020a03811660009081526004602052604090205460018114156109a357600160a060020a038216600081815260016020908152604080832080549084905580845260029092528083208054600160a060020a0319169055519092917f6381abe854c1429e636a1aa796dd6057d1f1e4836874fbb184650908c49804cc91a260035460606000805b838110156109855786600160a060020a03166003828154811015156108b657fe5b600091825260209091200154600160a060020a031614156108d657600191505b81151561092d5760038054829081106108eb57fe5b6000918252602090912001548351600160a060020a039091169084908390811061091157fe5b600160a060020a0390921660209283029091019091015261097d565b600380548290811061093b57fe5b6000918252602090912001548351600160a060020a03909116908490600019840190811061096557fe5b600160a060020a039092166020928302909101909101525b600101610895565b508151610999906003906020850190610cfd565b5050505050610b2c565b6001811115610b2757600160a060020a03821660008181526004602090815260408083205460018352818420819055835260029091528082208054600160a060020a03191684179055517fa010ae0edd95ff06bc66e3eacf9d4f39b23da7ae3056a38dd6c1dcd05630a6da9190a260035460606000805b83811015610b0a5785600160a060020a0316600382815481101515610a3b57fe5b600091825260209091200154600160a060020a03161415610a5b57600191505b811515610ab2576003805482908110610a7057fe5b6000918252602090912001548351600160a060020a0390911690849083908110610a9657fe5b600160a060020a03909216602092830290910190910152610b02565b6003805482908110610ac057fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610aea57fe5b600160a060020a039092166020928302909101909101525b600101610a1a565b508151610b1e906003906020850190610cfd565b50505050610b2c565b600080fd5b5050565b600054600160a060020a03165b90565b600054600160a060020a03163314610b5757600080fd5b600054600160a060020a0382811691161415610b7257600080fd5b60008054600160a060020a031916600160a060020a0392909216919091179055565b600081815260026020526040812054600160a060020a03161515610bba5750600061040e565b50600090815260026020526040902054600160a060020a031690565b331515610be257600080fd5b610bea610d62565b338152602081019283526040810191825242606082019081526005805460018101825560009190915291517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db060049093029283018054600160a060020a031916600160a060020a0390921691909117905592517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db182015590517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db282015590517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db390910155565b6003805482908110610cde57fe5b600091825260209091200154600160a060020a0316905081565b600190565b828054828255906000526020600020908101928215610d52579160200282015b82811115610d525782518254600160a060020a031916600160a060020a03909116178255602090920191600190910190610d1d565b50610d5e929150610d94565b5090565b6080604051908101604052806000600160a060020a031681526020016000815260200160008152602001600081525090565b610b3d91905b80821115610d5e578054600160a060020a0319168155600101610d9a56fea165627a7a723058204d04994059decc342e67452a38af95a3182beda6ea605bd2a105f4f9b3a7a2510029"
    # _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getStatus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_phoneNumber","type":"uint256"}],"name":"addRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"requests","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"cancelRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getNumber","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"applicant","type":"address"}],"name":"confirmRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_pn","type":"uint256"}],"name":"getAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_pn","type":"uint256"},{"name":"_value","type":"uint256"}],"name":"sendMoney","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"log","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"verify","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"pure","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationConfirmed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationConfirmed","type":"event"}]')
    return _bytecode, _abi

def phData():
    with open("PaymentHandler.bin", 'r') as bin:
        _bytecode = bin.read()
    with open("PaymentHandler.abi", 'r') as abi:
        _abi = json.loads(abi.read())
    # _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561018c8061003e6000396000f3fe608060405260043610610050577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c81146100525780639ee1bd0f14610067578063a6f9dae114610098575b005b34801561005e57600080fd5b506100506100cb565b34801561007357600080fd5b5061007c6100f0565b60408051600160a060020a039092168252519081900360200190f35b3480156100a457600080fd5b50610050600480360360208110156100bb57600080fd5b5035600160a060020a03166100ff565b600054600160a060020a031633146100e257600080fd5b600054600160a060020a0316ff5b600054600160a060020a031690565b600054600160a060020a0316331461011657600080fd5b600054600160a060020a038281169116141561013157600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039290921691909117905556fea165627a7a72305820526f825b0f9f8428b7535543052e096311f15a10c1a7ae2ddf550741af04d4df0029"
    # _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
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

def invokeContract(server, sender, contract, methodName, methodArgs, ni=0):

    _args = str(methodArgs)[1:-1]
    invoker = "contract.functions.{methodName}({methodArgs})".format(
        methodName=methodName,
        methodArgs=_args,
    )
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

    for k in len(fromTo):
        if fromTo[k]:
            time = setTime(times[k])
            print("{t} FROM: +{n} {v}".format(t=time, n=numbers[k], v=scaleValue(values[k])))
            
        elif not fromTo[k]:



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

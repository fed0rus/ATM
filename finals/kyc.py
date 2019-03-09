#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse

# -----------UTILS START------------

def initParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store", help="List all the requests")
    parser.add_argument("--confirm", action="store", help="Confirm the request")
    args = parser.parse_args()
    return vars(args)

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

def getUser(server, _privateKey):
    return server.eth.account.privateKeyToAccount(_privateKey)

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
    # _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a03191633179055610d798061003e6000396000f3fe608060405260043610610105576000357c01000000000000000000000000000000000000000000000000000000009004806383904f8d116100a75780639c8e149e116100765780639c8e149e146103755780639ee1bd0f1461038a578063a6f9dae11461039f578063f82c50f1146103d257610105565b806383904f8d146102e5578063851b16f5146102fa578063942ea4661461030f578063987fa1ed1461034257610105565b80634157272a116100e35780634157272a146101c55780634ca1fad8146102735780635a58cd4c1461029d57806374adad1d146102b257610105565b806309e6707d146101075780631d25899b1461014c57806330ccebb514610192575b005b34801561011357600080fd5b5061013a6004803603602081101561012a57600080fd5b5035600160a060020a03166103fc565b60408051918252519081900360200190f35b34801561015857600080fd5b506101766004803603602081101561016f57600080fd5b503561040e565b60408051600160a060020a039092168252519081900360200190f35b34801561019e57600080fd5b5061013a600480360360208110156101b557600080fd5b5035600160a060020a0316610429565b3480156101d157600080fd5b506101da610444565b604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b8381101561021e578181015183820152602001610206565b50505050905001838103825284818151815260200191508051906020019060200280838360005b8381101561025d578181015183820152602001610245565b5050505090500194505050505060405180910390f35b34801561027f57600080fd5b506101056004803603602081101561029657600080fd5b50356104d8565b3480156102a957600080fd5b506101056105ba565b3480156102be57600080fd5b5061013a600480360360208110156102d557600080fd5b5035600160a060020a03166105df565b3480156102f157600080fd5b506101056105f1565b34801561030657600080fd5b506101056106af565b34801561031b57600080fd5b5061013a6004803603602081101561033257600080fd5b5035600160a060020a0316610874565b34801561034e57600080fd5b506101056004803603602081101561036557600080fd5b5035600160a060020a031661088f565b34801561038157600080fd5b506101da610bcd565b34801561039657600080fd5b50610176610c38565b3480156103ab57600080fd5b50610105600480360360208110156103c257600080fd5b5035600160a060020a0316610c48565b3480156103de57600080fd5b50610176600480360360208110156103f557600080fd5b5035610c9c565b60016020526000908152604090205481565b600260205260009081526040902054600160a060020a031681565b600160a060020a031660009081526004602052604090205490565b6003546060908190818060005b838110156104cd5760016004600060038481548110151561046e57fe5b6000918252602080832090910154600160a060020a0316835282019290925260400190205411156104c55760038054829081106104a757fe5b6000918252602090912001548351600160a060020a03909116908490fe5b600101610451565b509093509150509091565b3315156104e457600080fd5b6402540be40081101580156104fe575064174876e7ff8111155b151561050957600080fd5b336000908152600460205260409020541561052357600080fd5b336000908152600160205260409020541561053d57600080fd5b33600081815260046020526040808220849055517fdc79fc57451962cfe3916e686997a49229af75ce2055deb4c0f0fdf3d5d2e7c19190a250600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b600054600160a060020a031633146105d157600080fd5b600054600160a060020a0316ff5b60046020526000908152604090205481565b3315156105fd57600080fd5b336000908152600460205260409020541561061757600080fd5b33600090815260016020526040902054151561063257600080fd5b3360008181526004602052604080822060019055517f64ed2364f9ee0643b60aeffba4ace8805648fad0d546c5efd449d1de10c8dcee9190a2600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b3315156106bb57600080fd5b3360009081526004602052604090205415156106d657600080fd5b33600090815260046020526040812054600114156106f2575060015b3360009081526004602052604081205580156107385760405133907f8c08d387d1333f3da7e980dd7fc958615d513ca73155b6dd2a5a13e17acd116290600090a2610764565b60405133907fffdf549003cf56ac2e863a28d8d5191467cf2a6d5e659f6a649e855a3d8cd8d090600090a25b60035460606000805b8381101561085957600380543391908390811061078657fe5b600091825260209091200154600160a060020a031614156107aa5760019150610851565b8115156108015760038054829081106107bf57fe5b6000918252602090912001548351600160a060020a03909116908490839081106107e557fe5b600160a060020a03909216602092830290910190910152610851565b600380548290811061080f57fe5b6000918252602090912001548351600160a060020a03909116908490600019840190811061083957fe5b600160a060020a039092166020928302909101909101525b60010161076d565b50815161086d906003906020850190610cc4565b5050505050565b600160a060020a031660009081526001602052604090205490565b600054600160a060020a031633146108a657600080fd5b600160a060020a0381166000908152600460205260409020546001811415610a4057600160a060020a038216600081815260016020908152604080832080549084905580845260029092528083208054600160a060020a0319169055519092917f6381abe854c1429e636a1aa796dd6057d1f1e4836874fbb184650908c49804cc91a260035460606000805b83811015610a225786600160a060020a031660038281548110151561095357fe5b600091825260209091200154600160a060020a0316141561097357600191505b8115156109ca57600380548290811061098857fe5b6000918252602090912001548351600160a060020a03909116908490839081106109ae57fe5b600160a060020a03909216602092830290910190910152610a1a565b60038054829081106109d857fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610a0257fe5b600160a060020a039092166020928302909101909101525b600101610932565b508151610a36906003906020850190610cc4565b5050505050610bc9565b6001811115610bc457600160a060020a03821660008181526004602090815260408083205460018352818420819055835260029091528082208054600160a060020a03191684179055517fa010ae0edd95ff06bc66e3eacf9d4f39b23da7ae3056a38dd6c1dcd05630a6da9190a260035460606000805b83811015610ba75785600160a060020a0316600382815481101515610ad857fe5b600091825260209091200154600160a060020a03161415610af857600191505b811515610b4f576003805482908110610b0d57fe5b6000918252602090912001548351600160a060020a0390911690849083908110610b3357fe5b600160a060020a03909216602092830290910190910152610b9f565b6003805482908110610b5d57fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610b8757fe5b600160a060020a039092166020928302909101909101525b600101610ab7565b508151610bbb906003906020850190610cc4565b50505050610bc9565b600080fd5b5050565b6003546060908190818060005b838110156104cd5760046000600383815481101515610bf557fe5b6000918252602080832090910154600160a060020a0316835282019290925260400190205460011415610c305760038054829081106104a757fe5b600101610bda565b600054600160a060020a03165b90565b600054600160a060020a03163314610c5f57600080fd5b600054600160a060020a0382811691161415610c7a57600080fd5b60008054600160a060020a031916600160a060020a0392909216919091179055565b6003805482908110610caa57fe5b600091825260209091200154600160a060020a0316905081565b828054828255906000526020600020908101928215610d19579160200282015b82811115610d195782518254600160a060020a031916600160a060020a03909116178255602090920191600190910190610ce4565b50610d25929150610d29565b5090565b610c4591905b80821115610d25578054600160a060020a0319168155600101610d2f56fea165627a7a723058202e52f7bc564e1e83adeafb45cac989db43f75ddc277a0dc40482640ddd882dc70029"
    # _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getStatus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"listAdd","outputs":[{"name":"","type":"address[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_phoneNumber","type":"uint256"}],"name":"addRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"requests","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"cancelRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getNumber","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"applicant","type":"address"}],"name":"confirmRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"listDel","outputs":[{"name":"","type":"address[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"log","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationConfirmed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationConfirmed","type":"event"}]')
    return _bytecode, _abi

def phData():
    with open("PaymentHandler.bin", 'r') as bin:
        _bytecode = bin.read()
    with open("PaymentHandler.abi", 'r') as abi:
        _abi = json.loads(abi.read())
    # _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561018c8061003e6000396000f3fe608060405260043610610050577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c81146100525780639ee1bd0f14610067578063a6f9dae114610098575b005b34801561005e57600080fd5b506100506100cb565b34801561007357600080fd5b5061007c6100f0565b60408051600160a060020a039092168252519081900360200190f35b3480156100a457600080fd5b50610050600480360360208110156100bb57600080fd5b5035600160a060020a03166100ff565b600054600160a060020a031633146100e257600080fd5b600054600160a060020a0316ff5b600054600160a060020a031690565b600054600160a060020a0316331461011657600080fd5b600054600160a060020a038281169116141561013157600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039290921691909117905556fea165627a7a72305820526f825b0f9f8428b7535543052e096311f15a10c1a7ae2ddf550741af04d4df0029"
    # _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    return _bytecode, _abi

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

def isContract(contract):
    stub, abi = kycData()
    return contract.abi == abi

# ------------UTILS END-------------

def listAdd(server):
    _contract = getContract(server, flag="kyc")
    addresses, numbers = callContract(_contract, methodName="listAdd")
    print(addresses)
    print(numbers)

# ----------MAIN MUTEX------------

if __name__ == "__main__":

    # ----------START SET------------

    with open("network.json", 'r') as ethConfig:
        global _defaultGasPrice
        global _gasPriceURL
        global _rpcURL
        global _privateKey
        read = json.load(ethConfig)
        _rpcURL = str(read["rpcUrl"])
        _privateKey = str(read["privKey"])
        _gasPriceURL = str(read["gasPriceUrl"])
        _defaultGasPrice = str(read["defaultGasPrice"])

    args = initParser()
    server = Web3(HTTPProvider(_rpcURL))
    user = getUser(server, _privateKey)

    # -----------END SET-------------

    if args["list"] is not None:
        listAdd(server)

#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse

# -----------UTILS START------------

HexBytes = lambda x: x

def initParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("--owner", action="store", help="Know the owner of the contract")
    global args
    args = parser.parse_args()
    return vars(args)

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
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a031916331790556104178061003e6000396000f3fe608060405260043610610098576000357c0100000000000000000000000000000000000000000000000000000000900480636c7f2b381161006b5780636c7f2b38146101485780637dba20b2146101985780639ee1bd0f146101cc578063a6f9dae1146101e157610098565b806309e6707d1461009a5780635a58cd4c146100ea57806362fe4707146100ff57806366c2a71014610133575b005b3480156100a657600080fd5b506100cd600480360360208110156100bd57600080fd5b5035600160a060020a0316610214565b60408051600160b060020a03199092168252519081900360200190f35b3480156100f657600080fd5b5061009861023f565b34801561010b57600080fd5b506100986004803603602081101561012257600080fd5b5035600160b060020a031916610264565b34801561013f57600080fd5b506100986102e8565b34801561015457600080fd5b5061017c6004803603602081101561016b57600080fd5b5035600160b060020a031916610356565b60408051600160a060020a039092168252519081900360200190f35b3480156101a457600080fd5b5061017c600480360360208110156101bb57600080fd5b5035600160b060020a031916610371565b3480156101d857600080fd5b5061017c610396565b3480156101ed57600080fd5b506100986004803603602081101561020457600080fd5b5035600160a060020a03166103a5565b6002602052600090815260409020547601000000000000000000000000000000000000000000000281565b600054600160a060020a0316331461025657600080fd5b600054600160a060020a0316ff5b33151561027057600080fd5b600160b060020a03198116600090815260016020908152604080832080543373ffffffffffffffffffffffffffffffffffffffff199091168117909155835260029091529020805469ffffffffffffffffffff1916760100000000000000000000000000000000000000000000909204919091179055565b336000908152600260209081526040808320805469ffffffffffffffffffff19811690915576010000000000000000000000000000000000000000000002600160b060020a031916835260019091529020805473ffffffffffffffffffffffffffffffffffffffff19169055565b600160205260009081526040902054600160a060020a031681565b600160b060020a031916600090815260016020526040902054600160a060020a031690565b600054600160a060020a031690565b600054600160a060020a031633146103bc57600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039290921691909117905556fea165627a7a723058202aadfa1786f8253e83ae9cbb6b9591320d934424f0a01398192e07d95a5ba9ca0029"
    _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"bytes10"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"phoneNumber","type":"bytes10"}],"name":"addCustomer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteCustomer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes10"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"number","type":"bytes10"}],"name":"getAddressByNumber","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    return _bytecode, _abi

def phData():
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905560b28061003d6000396000f3fe6080604052600436106038577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c8114603a575b005b348015604557600080fd5b50603860005473ffffffffffffffffffffffffffffffffffffffff163314606b57600080fd5b60005473ffffffffffffffffffffffffffffffffffffffff16fffea165627a7a723058204de0b629eddce83db5a57928cc08051753279fb7bb9f3900483226ae9308ff360029"
    _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    return _bytecode, _abi

def deployContract(server, owner, flag):
    # switch contract type
    if flag == "kyc":
        _bytecode, _abi = kycData()
    elif flag == "ph":
        _bytecode, _abi = phData()
    # deployment
    rawContract = server.eth.contract(abi=_abi, bytecode=_bytecode)
    _gas = rawContract.constructor().estimateGas({"from": owner.address})
    txUnsigned = rawContract.constructor().buildTransaction({
        "from": owner.address,
        "nonce": server.eth.getTransactionCount(owner.address),
        "gas": _gas,
        "gasPrice": getGasPrice(speed="fast"),
    })
    txSigned = owner.signTransaction(txUnsigned)
    deploymentHash = server.eth.sendRawTransaction(txSigned.rawTransaction)
    txReceipt = server.eth.waitForTransactionReceipt(deploymentHash)
    if txReceipt["status"] == 1:
        contractAddress = cleanTxResponse(txReceipt)["contractAddress"]
        contract = server.eth.contract(
            address=contractAddress,
            abi=_abi,
        )
        startBlock = cleanTxResponse(txReceipt)["blockNumber"]
        return contract.address, startBlock
    else:
        raise

def getContract(server, flag):

    with open("registrar.json", 'r') as db:
        data = json.load(db)
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

# -----------UTILS END------------

# ---------ESSENTIALS START---------

def deploy(server, owner):

    KYCAddress, sb1 = deployContract(server, owner, flag="kyc")
    PHAddress, sb2 = deployContract(server, owner, flag="ph")
    data = {
        "registrar": {
            "address": KYCAddress,
            "startBlock": sb1
        },
        "payments": {
            "address": PHAddress,
            "startBlock": sb2
        }
    }
    with open("registrar.json", 'w') as db:
        json.dump(data, db)
    print("KYC Registrar: {}".format(KYCAddress))
    print("Payment Handler: {}".format(PHAddress))

def returnOwner(server, flag):

    _contract = getContract(server, flag)
    ownerAddress = callContract(_contract, methodName="whoIsOwner")
    return ownerAddress


# ---------ESSENTIALS END---------


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

    if args["deploy"] is not False:
        deploy(server, user)

    elif args["owner"] is not None:
        if args["owner"] == "registrar":
            ownerAddress = returnOwner(server, flag="kyc")
            print("Admin account: {}".format(ownerAddress))
        elif args["owner"] == "payments":
            ownerAddress = returnOwner(server, flag="ph")
            print("Admin account: {}".format(ownerAddress))
        else:
            raise ValueError("Enter a valid contract type")


# compile: solc --abi --bin --optimize --overwrite -o ./ contract.sol

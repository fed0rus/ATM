#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse

def getUser(server, privateKey):
    return server.eth.account.privateKeyToAccount(privateKey)

# utils

HexBytes = lambda x: x

def getGasPrice(speed):
    try:
        response = requests.get(gasPriceURL)
        return int((response.json())[speed] * 1e9)
    except:
        return int(defaultGasPrice)

def cleanTxResponse(rawReceipt):
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

# essential

def deployContract(server, owner, flag):
    # switch contract type
    if flag == "kyc":
        _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561039f8061003e6000396000f3fe608060405260043610610050577c0100000000000000000000000000000000000000000000000000000000600035046303dd3d8181146100525780635a58cd4c146101055780636cf4f05a1461011a575b005b34801561005e57600080fd5b506100506004803603602081101561007557600080fd5b81019060208101813564010000000081111561009057600080fd5b8201836020820111156100a257600080fd5b803590602001918460018302840111640100000000831117156100c457600080fd5b91908080601f0160208091040260200160405190810160405280939291908181526020018383808284376000920191909152509295506101cf945050505050565b34801561011157600080fd5b506100506101ff565b34801561012657600080fd5b5061015a6004803603602081101561013d57600080fd5b503573ffffffffffffffffffffffffffffffffffffffff1661023e565b6040805160208082528351818301528351919283929083019185019080838360005b8381101561019457818101518382015260200161017c565b50505050905090810190601f1680156101c15780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b3315156101db57600080fd5b33600090815260016020908152604090912082516101fb928401906102d8565b5050565b60005473ffffffffffffffffffffffffffffffffffffffff16331461022357600080fd5b60005473ffffffffffffffffffffffffffffffffffffffff16ff5b60016020818152600092835260409283902080548451600294821615610100026000190190911693909304601f81018390048302840183019094528383529192908301828280156102d05780601f106102a5576101008083540402835291602001916102d0565b820191906000526020600020905b8154815290600101906020018083116102b357829003601f168201915b505050505081565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061031957805160ff1916838001178555610346565b82800160010185558215610346579182015b8281111561034657825182559160200191906001019061032b565b50610352929150610356565b5090565b61037091905b80821115610352576000815560010161035c565b9056fea165627a7a723058200310d5579140a59f073888aac1fc0fb1a97613009ce897b44f90c3ac14f0adc60029"
        _abi = json.loads('[{"constant":false,"inputs":[{"name":"phoneNumber","type":"string"}],"name":"addCustomer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"phonebook","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    elif flag == "ph":
        _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905560b28061003d6000396000f3fe6080604052600436106038577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c8114603a575b005b348015604557600080fd5b50603860005473ffffffffffffffffffffffffffffffffffffffff163314606b57600080fd5b60005473ffffffffffffffffffffffffffffffffffffffff16fffea165627a7a723058203256ff9f5ae4c2a972ee5608c13f802607ef898e0b363e6e7877d424386181480029"
        _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
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

def initParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    global args
    args = parser.parse_args()
    args = vars(args)

def main():

    initParser()
    with open("network.json", 'r') as ethConfig:
        global defaultGasPrice
        global gasPriceURL
        read = json.load(ethConfig)
        rpcURL = str(read["rpcUrl"])
        privateKey = str(read["privKey"])
        gasPriceURL = str(read["gasPriceUrl"])
        defaultGasPrice = str(read["defaultGasPrice"])
    server = Web3(HTTPProvider(rpcURL))
    owner = getUser(server, privateKey)
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

if __name__ == "__main__":
    main()

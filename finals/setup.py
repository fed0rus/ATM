#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse
import time

# -----------UTILS START------------

HexBytes = lambda x: x

def initParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("--owner", action="store", help="Know the owner of the contract")
    parser.add_argument("--chown", action="store", nargs='+', help="Change the owner of the contract")
    parser.add_argument("--send", action="store", nargs='+', help="Send money")
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
    with open("KYC.bin", 'r') as bin:
        _bytecode = bin.read()
    with open("KYC.abi", 'r') as abi:
        _abi = json.loads(abi.read())
    # _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a03191633179055610dc98061003e6000396000f3fe608060405260043610610110576000357c010000000000000000000000000000000000000000000000000000000090048063851b16f5116100a75780639ee1bd0f116100765780639ee1bd0f14610395578063a6f9dae1146103aa578063b93f9b0a146103dd578063f82c50f11461040757610110565b8063851b16f514610305578063942ea4661461031a578063987fa1ed1461034d5780639c8e149e1461038057610110565b80634ca1fad8116100e35780634ca1fad81461027e5780635a58cd4c146102a857806374adad1d146102bd57806383904f8d146102f057610110565b806309e6707d146101125780631d25899b1461015757806330ccebb51461019d5780634157272a146101d0575b005b34801561011e57600080fd5b506101456004803603602081101561013557600080fd5b5035600160a060020a0316610431565b60408051918252519081900360200190f35b34801561016357600080fd5b506101816004803603602081101561017a57600080fd5b5035610443565b60408051600160a060020a039092168252519081900360200190f35b3480156101a957600080fd5b50610145600480360360208110156101c057600080fd5b5035600160a060020a031661045e565b3480156101dc57600080fd5b506101e5610479565b604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b83811015610229578181015183820152602001610211565b50505050905001838103825284818151815260200191508051906020019060200280838360005b83811015610268578181015183820152602001610250565b5050505090500194505050505060405180910390f35b34801561028a57600080fd5b50610110600480360360208110156102a157600080fd5b503561050d565b3480156102b457600080fd5b506101106105ef565b3480156102c957600080fd5b50610145600480360360208110156102e057600080fd5b5035600160a060020a0316610614565b3480156102fc57600080fd5b50610110610626565b34801561031157600080fd5b506101106106e4565b34801561032657600080fd5b506101456004803603602081101561033d57600080fd5b5035600160a060020a03166108a9565b34801561035957600080fd5b506101106004803603602081101561037057600080fd5b5035600160a060020a03166108c4565b34801561038c57600080fd5b506101e5610c02565b3480156103a157600080fd5b50610181610c6d565b3480156103b657600080fd5b50610110600480360360208110156103cd57600080fd5b5035600160a060020a0316610c7d565b3480156103e957600080fd5b506101816004803603602081101561040057600080fd5b5035610cd1565b34801561041357600080fd5b506101816004803603602081101561042a57600080fd5b5035610cec565b60016020526000908152604090205481565b600260205260009081526040902054600160a060020a031681565b600160a060020a031660009081526004602052604090205490565b6003546060908190818060005b83811015610502576001600460006003848154811015156104a357fe5b6000918252602080832090910154600160a060020a0316835282019290925260400190205411156104fa5760038054829081106104dc57fe5b6000918252602090912001548351600160a060020a03909116908490fe5b600101610486565b509093509150509091565b33151561051957600080fd5b6402540be4008110158015610533575064174876e7ff8111155b151561053e57600080fd5b336000908152600460205260409020541561055857600080fd5b336000908152600160205260409020541561057257600080fd5b33600081815260046020526040808220849055517fdc79fc57451962cfe3916e686997a49229af75ce2055deb4c0f0fdf3d5d2e7c19190a250600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b600054600160a060020a0316331461060657600080fd5b600054600160a060020a0316ff5b60046020526000908152604090205481565b33151561063257600080fd5b336000908152600460205260409020541561064c57600080fd5b33600090815260016020526040902054151561066757600080fd5b3360008181526004602052604080822060019055517f64ed2364f9ee0643b60aeffba4ace8805648fad0d546c5efd449d1de10c8dcee9190a2600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b3315156106f057600080fd5b33600090815260046020526040902054151561070b57600080fd5b3360009081526004602052604081205460011415610727575060015b33600090815260046020526040812055801561076d5760405133907f8c08d387d1333f3da7e980dd7fc958615d513ca73155b6dd2a5a13e17acd116290600090a2610799565b60405133907fffdf549003cf56ac2e863a28d8d5191467cf2a6d5e659f6a649e855a3d8cd8d090600090a25b60035460606000805b8381101561088e5760038054339190839081106107bb57fe5b600091825260209091200154600160a060020a031614156107df5760019150610886565b8115156108365760038054829081106107f457fe5b6000918252602090912001548351600160a060020a039091169084908390811061081a57fe5b600160a060020a03909216602092830290910190910152610886565b600380548290811061084457fe5b6000918252602090912001548351600160a060020a03909116908490600019840190811061086e57fe5b600160a060020a039092166020928302909101909101525b6001016107a2565b5081516108a2906003906020850190610d14565b5050505050565b600160a060020a031660009081526001602052604090205490565b600054600160a060020a031633146108db57600080fd5b600160a060020a0381166000908152600460205260409020546001811415610a7557600160a060020a038216600081815260016020908152604080832080549084905580845260029092528083208054600160a060020a0319169055519092917f6381abe854c1429e636a1aa796dd6057d1f1e4836874fbb184650908c49804cc91a260035460606000805b83811015610a575786600160a060020a031660038281548110151561098857fe5b600091825260209091200154600160a060020a031614156109a857600191505b8115156109ff5760038054829081106109bd57fe5b6000918252602090912001548351600160a060020a03909116908490839081106109e357fe5b600160a060020a03909216602092830290910190910152610a4f565b6003805482908110610a0d57fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610a3757fe5b600160a060020a039092166020928302909101909101525b600101610967565b508151610a6b906003906020850190610d14565b5050505050610bfe565b6001811115610bf957600160a060020a03821660008181526004602090815260408083205460018352818420819055835260029091528082208054600160a060020a03191684179055517fa010ae0edd95ff06bc66e3eacf9d4f39b23da7ae3056a38dd6c1dcd05630a6da9190a260035460606000805b83811015610bdc5785600160a060020a0316600382815481101515610b0d57fe5b600091825260209091200154600160a060020a03161415610b2d57600191505b811515610b84576003805482908110610b4257fe5b6000918252602090912001548351600160a060020a0390911690849083908110610b6857fe5b600160a060020a03909216602092830290910190910152610bd4565b6003805482908110610b9257fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610bbc57fe5b600160a060020a039092166020928302909101909101525b600101610aec565b508151610bf0906003906020850190610d14565b50505050610bfe565b600080fd5b5050565b6003546060908190818060005b838110156105025760046000600383815481101515610c2a57fe5b6000918252602080832090910154600160a060020a0316835282019290925260400190205460011415610c655760038054829081106104dc57fe5b600101610c0f565b600054600160a060020a03165b90565b600054600160a060020a03163314610c9457600080fd5b600054600160a060020a0382811691161415610caf57600080fd5b60008054600160a060020a031916600160a060020a0392909216919091179055565b600090815260026020526040902054600160a060020a031690565b6003805482908110610cfa57fe5b600091825260209091200154600160a060020a0316905081565b828054828255906000526020600020908101928215610d69579160200282015b82811115610d695782518254600160a060020a031916600160a060020a03909116178255602090920191600190910190610d34565b50610d75929150610d79565b5090565b610c7a91905b80821115610d75578054600160a060020a0319168155600101610d7f56fea165627a7a72305820eab55b841a75ceff9a96a6be51ba58f4cd800d494b044425cfcad988d5ec999e0029"
    # _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getStatus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"listAdd","outputs":[{"name":"","type":"address[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_phoneNumber","type":"uint256"}],"name":"addRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"requests","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"cancelRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getNumber","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"applicant","type":"address"}],"name":"confirmRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"listDel","outputs":[{"name":"","type":"address[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_pn","type":"uint256"}],"name":"getAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"log","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationConfirmed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationConfirmed","type":"event"}]')
    return _bytecode, _abi

def phData():
    with open("PaymentHandler.bin", 'r') as bin:
        _bytecode = bin.read()
    with open("PaymentHandler.abi", 'r') as abi:
        _abi = json.loads(abi.read())
    # _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561018c8061003e6000396000f3fe608060405260043610610050577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c81146100525780639ee1bd0f14610067578063a6f9dae114610098575b005b34801561005e57600080fd5b506100506100cb565b34801561007357600080fd5b5061007c6100f0565b60408051600160a060020a039092168252519081900360200190f35b3480156100a457600080fd5b50610050600480360360208110156100bb57600080fd5b5035600160a060020a03166100ff565b600054600160a060020a031633146100e257600080fd5b600054600160a060020a0316ff5b600054600160a060020a031690565b600054600160a060020a0316331461011657600080fd5b600054600160a060020a038281169116141561013157600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039290921691909117905556fea165627a7a72305820526f825b0f9f8428b7535543052e096311f15a10c1a7ae2ddf550741af04d4df0029"
    # _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    return _bytecode, _abi

def getValidator():
    ABI = json.loads('[{"constant":true,"inputs":[{"name":"c","type":"address"}],"name":"checkValidityKYC","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"c","type":"address"}],"name":"addValidationPH","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"c","type":"address"}],"name":"checkValidityPH","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"list","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"c","type":"address"}],"name":"addValidationKYC","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
    validator = server.eth.contract(address="0x050b86da4348aB90D3339108CDEA201435488BA9", abi=ABI)
    return validator

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
        validator = getValidator()
        if flag == "kyc":
            validity = invokeContract(server, owner, validator, methodName="addValidationKYC", methodArgs=[contract.address], ni=1)
        else:
            validity = invokeContract(server, owner, validator, methodName="addValidationPH", methodArgs=[contract.address], ni=1)
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

def changeOwner(server, owner, newOwner, flag):
    assert server.isAddress(newOwner), "SWW"
    _contract = getContract(server, flag)
    txHash = invokeContract(server, owner, _contract, methodName="changeOwner", methodArgs=[newOwner])

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

    # US-001
    if args["deploy"] is not False:
        deploy(server, user)

    # US-002
    elif args["owner"] is not None:
        if args["owner"] == "registrar":
            ownerAddress = returnOwner(server, flag="kyc")
            print("Admin account: {}".format(ownerAddress))
        elif args["owner"] == "payments":
            ownerAddress = returnOwner(server, flag="ph")
            print("Admin account: {}".format(ownerAddress))
        else:
            raise ValueError("Enter a valid contract type")

    # US-003
    elif args["chown"] is not None:

        if args["chown"][0] == "registrar":
            try:
                newAdminAccount = args["chown"][1]
                changeOwner(server, user, newOwner=newAdminAccount, flag="kyc")
                print("New admin account: {}".format(newAdminAccount))
            except:
                print("Request cannot be executed")
        elif args["chown"][0] == "payments":
            try:
                newAdminAccount = args["chown"][1]
                changeOwner(server, user, newOwner=newAdminAccount, flag="ph")
                print("New admin account: {}".format(newAdminAccount))
            except:
                print("Request cannot be executed")
        else:
            raise ValueError("Enter a valid contract type")

'''
compile:
    solc --abi --bin --optimize --overwrite -o ./ KYCRegistrar.sol && solc --abi --bin --optimize --overwrite -o ./ PaymentHandler.sol
'''

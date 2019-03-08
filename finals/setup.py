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
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a031916331790556105b68061003e6000396000f3fe6080604052600436106100c4576000357c01000000000000000000000000000000000000000000000000000000009004806383904f8d1161008157806383904f8d146101f6578063851b16f51461020b5780639ee1bd0f14610220578063a6f9dae114610235578063e5b1863014610268578063e9238cc41461029b576100c4565b806309e6707d146100c65780631d25899b1461010b57806330ccebb5146101515780634ca1fad8146101845780635a58cd4c146101ae57806374adad1d146101c3575b005b3480156100d257600080fd5b506100f9600480360360208110156100e957600080fd5b5035600160a060020a03166102c5565b60408051918252519081900360200190f35b34801561011757600080fd5b506101356004803603602081101561012e57600080fd5b50356102d7565b60408051600160a060020a039092168252519081900360200190f35b34801561015d57600080fd5b506100f96004803603602081101561017457600080fd5b5035600160a060020a03166102f2565b34801561019057600080fd5b506100c4600480360360208110156101a757600080fd5b503561030d565b3480156101ba57600080fd5b506100c4610393565b3480156101cf57600080fd5b506100f9600480360360208110156101e657600080fd5b5035600160a060020a03166103b8565b34801561020257600080fd5b506100c46103ca565b34801561021757600080fd5b506100c461042c565b34801561022c57600080fd5b506101356104e4565b34801561024157600080fd5b506100c46004803603602081101561025857600080fd5b5035600160a060020a03166104f3565b34801561027457600080fd5b506100f96004803603602081101561028b57600080fd5b5035600160a060020a0316610554565b3480156102a757600080fd5b50610135600480360360208110156102be57600080fd5b503561056f565b60026020526000908152604090205481565b600160205260009081526040902054600160a060020a031681565b600160a060020a031660009081526003602052604090205490565b33151561031957600080fd5b6402540be4008110158015610333575064174876e7ff8111155b151561033e57600080fd5b336000908152600360205260409020541561035857600080fd5b33600081815260036020526040808220849055517fdc79fc57451962cfe3916e686997a49229af75ce2055deb4c0f0fdf3d5d2e7c19190a250565b600054600160a060020a031633146103aa57600080fd5b600054600160a060020a0316ff5b60036020526000908152604090205481565b3315156103d657600080fd5b3360009081526002602052604090205415156103f157600080fd5b3360008181526003602052604080822060019055517f64ed2364f9ee0643b60aeffba4ace8805648fad0d546c5efd449d1de10c8dcee9190a2565b33151561043857600080fd5b33600090815260036020526040902054151561045357600080fd5b336000908152600360205260408120546001141561046f575060015b3360009081526003602052604081205580156104b55760405133907f8c08d387d1333f3da7e980dd7fc958615d513ca73155b6dd2a5a13e17acd116290600090a26104e1565b60405133907fffdf549003cf56ac2e863a28d8d5191467cf2a6d5e659f6a649e855a3d8cd8d090600090a25b50565b600054600160a060020a031690565b600054600160a060020a0316331461050a57600080fd5b600054600160a060020a038281169116141561052557600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a0392909216919091179055565b600160a060020a031660009081526002602052604090205490565b600090815260016020526040902054600160a060020a03169056fea165627a7a723058203089412182edbb3c5dce3a0ea2d8c6e3fe2b811d2f29f6018a567a9c0a441b940029"
    _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getStatus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_phoneNumber","type":"uint256"}],"name":"addRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"requests","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"cancelRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getNumberByAddress","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_number","type":"uint256"}],"name":"getAddressByNumber","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationCanceled","type":"event"}]')
    return _bytecode, _abi

def phData():
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561018c8061003e6000396000f3fe608060405260043610610050577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c81146100525780639ee1bd0f14610067578063a6f9dae114610098575b005b34801561005e57600080fd5b506100506100cb565b34801561007357600080fd5b5061007c6100f0565b60408051600160a060020a039092168252519081900360200190f35b3480156100a457600080fd5b50610050600480360360208110156100bb57600080fd5b5035600160a060020a03166100ff565b600054600160a060020a031633146100e257600080fd5b600054600160a060020a0316ff5b600054600160a060020a031690565b600054600160a060020a0316331461011657600080fd5b600054600160a060020a038281169116141561013157600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039290921691909117905556fea165627a7a72305820526f825b0f9f8428b7535543052e096311f15a10c1a7ae2ddf550741af04d4df0029"
    _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
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

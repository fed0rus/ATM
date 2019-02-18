#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse

def getPrivateKey():
    with open("account.json", 'r') as acc:
        return str(json.load(acc)["account"])

def getUser(server, privateKey):
    return server.eth.account.privateKeyToAccount(privateKey)

# utils

HexBytes = lambda x: x

def getGasPrice(speed):
    response = requests.get("https://gasprice.poa.network")
    return int((response.json())[speed] * 1e9)

def cleanTxResponse(rawReceipt):
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

# essential

def deployContract(server, owner):

    with open("KYC.bin", 'r') as binFile:
        _bytecode = binFile.read()
    with open("KYC.abi", 'r') as abiFile:
        _abi = json.loads(abiFile.read())

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
        data = {
            "registrar": contract.address,
            "startBlock": startBlock,
        }
        with open("database.json", 'w') as db:
            json.dump(data, db)
        return contract
    else:
        raise

def invokeContract(server, sender, contract, methodName, methodArgs):

    _args = str(methodArgs)[1:-1]
    invoker = "contract.functions.{methodName}({methodArgs})".format(
        methodName=methodName,
        methodArgs=_args,
    )
    _gas = eval(invoker).estimateGas({"from": owner.address})
    txUnsigned = eval(invoker).buildTransaction({
        "from": sender.address,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gas": _gas,
        "gasPrice": getGasPrice(speed="fast"),
    })
    txSigned = sender.signTransaction(txUnsigned)
    txHash = server.eth.sendRawTransaction(txSigned.rawTransaction).hex()
    return txHash

def callContract(contract, methodName, methodArgs):

    _args = str(methodArgs)[1:-1]
    response = "contract.functions.{methodName}({methodArgs})".format(
        methodName=methodName,
        methodArgs=_args,
    )
    return response

def getContract(server, owner):

    with open("database.json", 'r') as db:
        data = json.load(db)
    with open("KYC.abi", 'r') as abiFile:
        _abi = json.loads(abiFile.read())
    contractAddress = data["registrar"]
    _contract = server.eth.contract(address=contractAddress, abi=_abi)
    return _contract

def initParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("--add", action="store", nargs='+', help="Bind your name with your address")
    parser.add_argument("--del", action="store_true", help="Unbind your name from your address")
    parser.add_argument("--getacc", action="store", nargs='+', help="Retrieve the addresses binded with your name")
    parser.add_argument("--getname", action="store", help="Retrieve the name binded with your address")
    parser.add_argument("--list", action="store_true", help="List all customers")
    global args
    args = parser.parse_args()
    args = vars(args)
    if args["add"] is not None:
        if len(args["add"]) > 1:
            args["add"] = ' '.join(args["add"])
        else:
            args["add"] = str(args["add"][0])
    if args["getacc"] is not None:
        if len(args["getacc"]) > 1:
            args["getacc"] = ' '.join(args["getacc"])
        else:
            args["getacc"] = str(args["getacc"][0])

# main mutex
def handleArgs(server, owner):
    # US 01-02
    if args["deploy"] is True:
        contract = deployContract(server, owner)
        print("Contract address: {0}".format(contract.address))

    # US 03-06
    elif args["add"] is not None:
        _contract = getContract(server, owner)
        flag = callContract(
            contract=_contract,
            methodName="isAddressUsed",
            methodArgs=[owner.address],
        )
        if not flag:
        # try:
            txHash = invokeContract(
                server=server,
                sender=owner,
                contract=_contract,
                methodName="addCustomer",
                methodArgs=[args["add"].encode("utf-8")],
            )
            print("Successfully added by {tx}".format(tx=txHash))
        # except ValueError:
        #     print("No enough funds to add name")
        # except:
        #     print("Name is too long, must be less or equal 32 characters including spaces")
        else:
            print("One account must correspond one name")

    # US 07-10
    elif args["del"] is True:
        _contract = getContract(server, owner)
        flag = callContract(
            contract=_contract,
            methodName="isAddressUsed",
            methodArgs=[owner.address],
        )
        if flag:
            try:
                txHash = invokeContract(
                    server=server,
                    sender=owner,
                    contract=_contract,
                    methodSig="deleteCustomer()",
                    methodName="deleteCustomer",
                    methodArgs=[],
                    methodArgsTypes=[],
                )
                if len(txHash) == 66:
                    print("Successfully deleted by {tx}".format(tx=txHash))
                else:
                    print("Error while invoking the contract was occured")
            except ValueError:
                    print("No enough funds to delete name")
        else:
            print("No name found for your account")

    # US 11-13
    elif args["getacc"] is not None:
        try:
            addresses = callContract(
                contract=getContract(server, owner),
                methodName="retrieveAddresses",
                methodArgs=[args["getacc"].encode("utf-8")],
            )
            if len(addresses) == 1:
                print("Registered account is {addr}".format(addr=addresses[0]))
            elif len(addresses) == 0:
                print("No account registered for this name")
            else:
                print("Registered accounts are:")
                for addr in addresses:
                    print(addr)
        except:
            print("Name is too long, must be less or equal 32 characters including spaces")

    # US 14-16
    elif args["getname"] is not None:
        _nameRaw = callContract(
            contract=getContract(server, owner),
            methodName="retrieveName",
            methodArgs=[server.toChecksumAddress(args["getname"])]
        ).decode("utf-8")
        _name = ""
        for letter in _nameRaw:
            if (ord(letter) != 0):
                _name += letter
        if _name != "":
            print("Registered account is \"{name}\"".format(name=_name))
        else:
            print("No name registered for this account")
    elif args["list"] is True:
        addresses, names = callContract(
                contract=getContract(server, owner),
                methodName="listAllAddresses",
                methodArgs=[],
        )
        if (len(addresses) == 0):
            print("Storage is clear")
        else:
            pool = set()
            for i in range(len(addresses)):
                _nameRaw = names[i].decode("utf-8")
                _name = ""
                for letter in _nameRaw:
                    if (ord(letter) != 0):
                        _name += letter
                pool.add("\"{n}\": {a}".format(n=_name, a=addresses[i]))
            for k in pool:
                print(k)
    else:
        print("Enter a valid command")

# entry point
def main():
    initParser()
    server = Web3(HTTPProvider("https://sokol.poa.network"))
    owner = getUser(server, getPrivateKey())
    handleArgs(server, owner)

if __name__ == "__main__":
    main()

# abi: [{'constant': True, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'retrieveName', 'outputs': [{'name': '', 'type': 'bytes32'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'isAddressUsed', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'bytes32'}], 'name': 'addCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteContract', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'listAllAddresses', 'outputs': [{'name': '', 'type': 'address[]'}, {'name': '', 'type': 'bytes32[]'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'customerName', 'type': 'bytes32'}], 'name': 'retrieveAddresses', 'outputs': [{'name': '', 'type': 'address[]'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'}]
# DIR: cd .\Documents\Code\GitHub\fintech\ETC\contract

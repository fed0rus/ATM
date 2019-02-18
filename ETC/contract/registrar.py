#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse
from eth_account import Account

class Owner(object):
    def __init__(self, address, privateKey):
        self.address = address
        self.privateKey = privateKey

def extractPrivateKey():
    account = open("account.json", 'r')
    privateKey = eval(account.read())["account"]
    account.close()
    return privateKey

def generateAddressFromPrivateKey(privateKey):
    privateKey = "0x" + str(privateKey)
    return str((Account.privateKeyToAccount(privateKey)).address)

global _bytecode
global _abi
_bytecode = "608060405233151561001057600080fd5b60008054600160a060020a03191633179055610775806100316000396000f3006080604052600436106100985763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663026b599b811461009a578063394819fd146100cd578063569fdae7146100ee57806356b969c9146101235780635a58cd4c1461013b57806366c2a7101461015057806380a2eac4146101655780639272affe14610213578063ab83e3bf1461024a575b005b3480156100a657600080fd5b506100bb600160a060020a03600435166102b2565b60408051918252519081900360200190f35b3480156100d957600080fd5b506100bb600160a060020a03600435166102cd565b3480156100fa57600080fd5b5061010f600160a060020a03600435166102df565b604080519115158252519081900360200190f35b34801561012f57600080fd5b506100986004356102fc565b34801561014757600080fd5b5061009861039d565b34801561015c57600080fd5b506100986103c2565b34801561017157600080fd5b5061017a610544565b604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b838110156101be5781810151838201526020016101a6565b50505050905001838103825284818151815260200191508051906020019060200280838360005b838110156101fd5781810151838201526020016101e5565b5050505090500194505050505060405180910390f35b34801561021f57600080fd5b5061022e600435602435610600565b60408051600160a060020a039092168252519081900360200190f35b34801561025657600080fd5b50610262600435610637565b60408051602080825283518183015283519192839290830191858101910280838360005b8381101561029e578181015183820152602001610286565b505050509050019250505060405180910390f35b600160a060020a031660009081526001602052604090205490565b60016020526000908152604090205481565b600160a060020a0316600090815260016020526040902054151590565b33151561030857600080fd5b33321461031457600080fd5b3360008181526001602081815260408084208690559483526002815293822080548083018255908352938220909301805473ffffffffffffffffffffffffffffffffffffffff1990811684179091556003805494850181559091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b9092018054909216179055565b600054600160a060020a031633146103b457600080fd5b600054600160a060020a0316ff5b606060008080803315156103d557600080fd5b3332146103e157600080fd5b50503360009081526001602090815260408083208054908490558084526002909252822054909350909150815b8181101561051d57600084815260026020526040902080543391908390811061043357fe5b600091825260209091200154600160a060020a031614156104575760019250610515565b82156104bd57600084815260026020526040902080548290811061047757fe5b6000918252602090912001548551600160a060020a0390911690869060001984019081106104a157fe5b600160a060020a03909216602092830290910190910152610515565b60008481526002602052604090208054829081106104d757fe5b6000918252602090912001548551600160a060020a03909116908690839081106104fd57fe5b600160a060020a039092166020928302909101909101525b60010161040e565b6000848152600260209081526040909120865161053c928801906106a3565b505050505050565b60035460609081908190600081811015610596576001600060038381548110151561056b57fe5b6000918252602080832090910154600160a060020a0316835282019290925260400190205483518490fe5b600383818054806020026020016040519081016040528092919081815260200182805480156105ee57602002820191906000526020600020905b8154600160a060020a031681526001909101906020018083116105d0575b50505050509150945094505050509091565b60026020528160005260406000208181548110151561061b57fe5b600091825260209091200154600160a060020a03169150829050565b60008181526002602090815260409182902080548351818402810184019094528084526060939283018282801561069757602002820191906000526020600020905b8154600160a060020a03168152600190910190602001808311610679575b50505050509050919050565b828054828255906000526020600020908101928215610705579160200282015b82811115610705578251825473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039091161782556020909201916001909101906106c3565b50610711929150610715565b5090565b61074691905b8082111561071157805473ffffffffffffffffffffffffffffffffffffffff1916815560010161071b565b905600a165627a7a72305820a8cc615587c312c063abf8b5555f44118d4c4df58f775afd8c75c2e8d12043820029"
_abi = [{"constant":True,"inputs":[{"name":"customerAddress","type":"address"}],"name":"retrieveName","outputs":[{"name":"","type":"bytes32"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"addressToCustomerName","outputs":[{"name":"","type":"bytes32"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"customerAddress","type":"address"}],"name":"isAddressUsed","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"customerName","type":"bytes32"}],"name":"addCustomer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[],"name":"deleteContract","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[],"name":"deleteCustomer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"listAllAddresses","outputs":[{"name":"","type":"address[]"},{"name":"","type":"bytes32[]"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"","type":"bytes32"},{"name":"","type":"uint256"}],"name":"customerNameToAddress","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"customerName","type":"bytes32"}],"name":"retrieveAddresses","outputs":[{"name":"","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"payable":True,"stateMutability":"payable","type":"fallback"}]
# utils

HexBytes = lambda x: x

def getGasPrice(speed):
    response = requests.get("https://gasprice.poa.network")
    return int((response.json())[speed] * 1e9)

def cleanTxResponse(rawReceipt):
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

# essential

def deployContract(server, owner):
    rawKYC = server.eth.contract(abi=_abi, bytecode=_bytecode)
    tx = {
        "nonce": server.eth.getTransactionCount(owner.address),
        "gasPrice": getGasPrice(speed="fast"),
        "gas": 971523, # estimated properly
        "to": None,
        "value": 0,
        "data": rawKYC.bytecode
    }
    contractDeploymentTransactionSigned = server.eth.account.signTransaction(
        tx,
        extractPrivateKey()
    )
    deploymentHash = server.eth.sendRawTransaction(contractDeploymentTransactionSigned.rawTransaction)
    txReceipt = server.eth.waitForTransactionReceipt(deploymentHash)
    contractAddress = cleanTxResponse(txReceipt)["contractAddress"]
    contract = server.eth.contract(
        address=contractAddress,
        abi=_abi,
    )
    file = open("database.json", "w")
    startBlock = cleanTxResponse(txReceipt)["blockNumber"]
    file.write("{\"registrar\": \"%s\", \"startBlock\": %s}" % (contract.address, startBlock))
    file.close()
    return contract

def invokeContract(server, sender, contract, methodSig, methodName, methodArgs, methodArgsTypes, value=0):
    methodSignature = server.keccak(text=methodSig)[0:4].hex()
    params = encode_abi(methodArgsTypes, methodArgs)
    payloadData = "0x" + methodSignature + params.hex()
    rawTX = {
        "to": contract.address,
        "data": payloadData,
        "value": value,
        "from": sender.address,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gasPrice": getGasPrice(speed="fast"),
    }
    gas = server.eth.estimateGas(rawTX)
    # print("-------------------------GAS------------------------------")
    # print("                                                          ")
    # print("\t\t\t{g}".format(g=gas))
    # print("                                                          ")
    # print("-------------------------GAS------------------------------")
    rawTX["gas"] = gas
    signedTX = server.eth.account.signTransaction(
        rawTX,
        sender.privateKey,
    )
    txHash = server.eth.sendRawTransaction(signedTX.rawTransaction).hex()
    return txHash

def callContract(contract, methodName, methodArgs):
    _args = str(methodArgs)[1:-1]
    response = eval("contract.functions.{}({}).call()".format(methodName, _args))
    return response

def getContract(server, owner):
    # fetch contract address from database.json
    db = open("database.json", 'r')
    data = eval(db.read())
    db.close()
    contractAddress = data["registrar"]
    # generate contract abi
    _contract = server.eth.contract(address=contractAddress, abi=_abi)
    return _contract

def initParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("--add", action="store", nargs='+', help="Bind your name with current address")
    parser.add_argument("--del", action="store_true", help="Unbind your name from your address")
    parser.add_argument("--getacc", action="store", nargs='+', help="Retrieve the addresses binded with your name")
    parser.add_argument("--getname", action="store", help="Retrieve the name binded with your address")
    parser.add_argument("--list", action="store_true", help="List all customers")
    global args
    args = parser.parse_args()
    args = vars(args)
    if args["add"] is not None :
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
                methodSig="addCustomer(bytes32)",
                methodName="addCustomer",
                methodArgs=[args["add"].encode("utf-8")],
                methodArgsTypes=["bytes32"],
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
    owner = Owner(generateAddressFromPrivateKey(extractPrivateKey()), extractPrivateKey())
    handleArgs(server, owner)

if __name__ == "__main__":
    main()

# abi: [{'constant': True, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'retrieveName', 'outputs': [{'name': '', 'type': 'bytes32'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'isAddressUsed', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'bytes32'}], 'name': 'addCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteContract', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'listAllAddresses', 'outputs': [{'name': '', 'type': 'address[]'}, {'name': '', 'type': 'bytes32[]'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'customerName', 'type': 'bytes32'}], 'name': 'retrieveAddresses', 'outputs': [{'name': '', 'type': 'address[]'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'}]
# DIR: cd .\Documents\Code\GitHub\fintech\ETC\contract

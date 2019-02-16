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
_bytecode = "0x6080604052600073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415151561004057600080fd5b336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550610d1b8061008f6000396000f300608060405260043610610099576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063026b599b1461009b578063394819fd146100fa578063569fdae71461015957806356b969c9146101b45780635a58cd4c146101e557806366c2a710146101fc57806380a2eac4146102135780639272affe146102c7578063ab83e3bf14610342575b005b3480156100a757600080fd5b506100dc600480360381019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506103c8565b60405180826000191660001916815260200191505060405180910390f35b34801561010657600080fd5b5061013b600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610411565b60405180826000191660001916815260200191505060405180910390f35b34801561016557600080fd5b5061019a600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610429565b604051808215151515815260200191505060405180910390f35b3480156101c057600080fd5b506101e36004803603810190808035600019169060200190929190505050610479565b005b3480156101f157600080fd5b506101fa610651565b005b34801561020857600080fd5b506102116106e6565b005b34801561021f57600080fd5b50610228610a3f565b604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b8381101561026f578082015181840152602081019050610254565b50505050905001838103825284818151815260200191508051906020019060200280838360005b838110156102b1578082015181840152602081019050610296565b5050505090500194505050505060405180910390f35b3480156102d357600080fd5b50610300600480360381019080803560001916906020019092919080359060200190929190505050610b2c565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b34801561034e57600080fd5b506103716004803603810190808035600019169060200190929190505050610b79565b6040518080602001828103825283818151815260200191508051906020019060200280838360005b838110156103b4578082015181840152602081019050610399565b505050509050019250505060405180910390f35b6000600160008373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020549050919050565b60016020528060005260406000206000915090505481565b600080600160008473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020546001900414159050919050565b600073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141515156104b557600080fd5b3273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156104ef57600080fd5b80600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002081600019169055506002600082600019166000191681526020019081526020016000203390806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505060033390806001815401808255809150509060018203906000526020600020016000909192909190916101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050600481908060018154018082558091505090600182039060005260206000200160009091929091909150906000191690555050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156106ac57600080fd5b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16ff5b6060600080600080600073ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415151561072a57600080fd5b3273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561076457600080fd5b600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000205493506000600102600160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020816000191690555060009250600260008560001916600019168152602001908152602001600020805490509150600090505b81811015610a08573373ffffffffffffffffffffffffffffffffffffffff166002600086600019166000191681526020019081526020016000208281548110151561086357fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1614156108b357600192506109fd565b821561095e57600260008560001916600019168152602001908152602001600020818154811015156108e157fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16856001830381518110151561091d57fe5b9060200190602002019073ffffffffffffffffffffffffffffffffffffffff16908173ffffffffffffffffffffffffffffffffffffffff16815250506109fc565b6002600085600019166000191681526020019081526020016000208181548110151561098657fe5b9060005260206000200160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1685828151811015156109bf57fe5b9060200190602002019073ffffffffffffffffffffffffffffffffffffffff16908173ffffffffffffffffffffffffffffffffffffffff16815250505b5b80600101905061081c565b846002600086600019166000191681526020019081526020016000209080519060200190610a37929190610c22565b505050505050565b6060806003600481805480602002602001604051908101604052809291908181526020018280548015610ac757602002820191906000526020600020905b8160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019060010190808311610a7d575b5050505050915080805480602002602001604051908101604052809291908181526020018280548015610b1d57602002820191906000526020600020905b81546000191681526020019060010190808311610b05575b50505050509050915091509091565b600260205281600052604060002081815481101515610b4757fe5b906000526020600020016000915091509054906101000a900473ffffffffffffffffffffffffffffffffffffffff1681565b6060600260008360001916600019168152602001908152602001600020805480602002602001604051908101604052809291908181526020018280548015610c1657602002820191906000526020600020905b8160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019060010190808311610bcc575b50505050509050919050565b828054828255906000526020600020908101928215610c9b579160200282015b82811115610c9a5782518260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555091602001919060010190610c42565b5b509050610ca89190610cac565b5090565b610cec91905b80821115610ce857600081816101000a81549073ffffffffffffffffffffffffffffffffffffffff021916905550600101610cb2565b5090565b905600a165627a7a723058205453fcbdf0a66c80ddbf106fc9c85b1f2aa626b2656cc765d3e8f345e1202fbe0029"
_abi = [{'constant': True, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'retrieveName', 'outputs': [{'name': '', 'type': 'bytes32'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'customerAddress', 'type': 'address'}], 'name': 'isAddressUsed', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'name': 'customerName', 'type': 'bytes32'}], 'name': 'addCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteContract', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': False, 'inputs': [], 'name': 'deleteCustomer', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'listAllAddresses', 'outputs': [{'name': '', 'type': 'address[]'}, {'name': '', 'type': 'bytes32[]'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [{'name': 'customerName', 'type': 'bytes32'}], 'name': 'retrieveAddresses', 'outputs': [{'name': '', 'type': 'address[]'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'payable': True, 'stateMutability': 'payable', 'type': 'fallback'}]

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
    methodSignature = server.sha3(text=methodSig)[0:4].hex()
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
    if args["add"] is not None and len(args["add"]) > 1:
        args["add"] = ' '.join(args["add"])
    elif args["getacc"] is not None and len(args["getacc"]) > 1:
        args["getacc"] = ' '.join(args["getacc"])

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
            try:
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
            except ValueError:
                print("No enough funds to add name")
            except:
                print("Name is too long, must be less or equal 32 characters including spaces")
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

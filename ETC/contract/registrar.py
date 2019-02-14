from eth_abi import encode_abi
import json
import requests
from solc import compile_source
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

def getContractSource(ownerAddress):
    soliditySource = '''
    pragma solidity ^0.4.25;

    contract Mortal {
        address owner;

        constructor() public {
            require(%s != address(0));
            owner = %s;
        }

        modifier ownerOnly {
            require(msg.sender == owner);
            _;
        }
    }

    contract KYC is Mortal {

        address[] addresses;
        bytes32[] names;

        function addCustomer(bytes32 customerName) public {
            require(msg.sender != address(0));
            require(msg.sender == tx.origin);
            addresses.push(msg.sender);
            names.push(customerName);
        }

        function deleteCustomer() public {
            require(msg.sender != address(0));
            require(msg.sender == tx.origin);
            address[] memory moveAddresses;
            bytes32[] memory moveNames;
            bool shift = false;
            for (uint i = 0; i < addresses.length; ++i) {
                if (addresses[i] == msg.sender) {
                    shift = true;
                }
                else {
                    if (shift == false) {
                        moveAddresses[i] = addresses[i];
                        moveNames[i] = names[i];
                    }
                    else {
                        moveAddresses[i - 1] = addresses[i];
                        moveNames[i - 1] = names[i];
                    }
                }
            }
            addresses = moveAddresses;
            names = moveNames;
        }

        function retrieveName(address customerAddress) external view returns (bytes32) {
            for (uint i = 0; i < addresses.length; ++i) {
                if (addresses[i] == customerAddress) {
                    return names[i];
                }
            }
        }

        function retrieveAddresses(bytes32 customerName) external view returns (address[]) {
            address[] memory response;
            for (uint i = 0; i < names.length; ++i) {
                if (names[i] == customerName) {
                    response[response.length] = addresses[i];
                }
            }
            return response;
        }

        function listAllAddresses() external view returns (address[], bytes32[]) {
            return (addresses, names);
        }

        function isAddressUsed(address customerAddress) external view returns (bool) {
            for (uint i = 0; i < addresses.length; ++i) {
                if (addresses[i] == customerAddress) {
                    return true;
                }
            }
            return false;
        }

        function () external payable {}

        function deleteContract() external ownerOnly {
            selfdestruct(address(owner));
        }
    }
    ''' % (ownerAddress, ownerAddress)
    return soliditySource

# utils

HexBytes = lambda x: x

def getGasPrice(speed):
    response = requests.get("https://gasprice.poa.network")
    return int((response.json())[speed] * 1e9)

def cleanTxResponse(rawReceipt):
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

# essential

def deployContract(server, owner):
    contractData = {}
    contractSource = getContractSource(owner.address)
    compiledSource = compile_source(contractSource)
    contractInterface = compiledSource["<stdin>:KYC"]
    contractData["abi"] = contractInterface['abi']
    rawKYC = server.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
    gasCost = server.eth.estimateGas({"to": None, "value": 0, "data": rawKYC.bytecode})
    tx = {
        "nonce": server.eth.getTransactionCount(owner.address),
        "gasPrice": getGasPrice(speed="fast"),
        "gas": gasCost,
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
    contractData["contractAddress"] = cleanTxResponse(txReceipt)["contractAddress"]
    contract = server.eth.contract(
        address=contractData["contractAddress"],
        abi=contractData["abi"],
    )
    file = open("database.json", "w+")
    startBlock = cleanTxResponse(txReceipt)["blockNumber"]
    dataToStore = {
        "registrar": contract.address,
        "startBlock": startBlock,
    }
    file.write(str(dataToStore))
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
    print("------------------------GAS------------------------------")
    print(gas)
    print("------------------------GAS------------------------------")
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
    contractSource = getContractSource(owner.address)
    compiledSource = compile_source(contractSource)
    contractInterface = compiledSource["<stdin>:KYC"]
    _abi = contractInterface['abi']
    _contract = server.eth.contract(address=contractAddress, abi=_abi)
    return _contract

def initParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("--add", action="store", help="Bind your name with current address")
    parser.add_argument("--del", action="store_true", help="Unbind your name from your address")
    parser.add_argument("--getacc", action="store", help="Retrieve the addresses binded with your name")
    parser.add_argument("--getname", action="store", help="Retrieve the name binded with your address")
    parser.add_argument("--list", action="store_true", help="List all customers")
    global args
    args = parser.parse_args()
    args = vars(args)

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
        for i in range(len(addresses)):
            _nameRaw = names[i].decode("utf-8")
            _name = ""
            for letter in _nameRaw:
                if (ord(letter) != 0):
                    _name += letter
            print("\"{n}\": {a}".format(n=_name, a=addresses[i]))
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
# CA: 0x7CC4B7c250B5E6db9b281679f3baa0d163000b8c
# DIR: cd .\Documents\Code\GitHub\fintech\ETC\contract

from eth_abi import encode_abi
import json
import sys
import time
import requests
from web3 import Web3, HTTPProvider
import utilities

ethConfig = utilities.net()
global server
global PRIVATE_KEY
global DEFAULT_GAS_PRICE
global GAS_URL
PRIVATE_KEY = ethConfig["privKey"]
DEFAULT_GAS_PRICE = ethConfig["defaultGasPrice"]
GAS_URL = ethConfig["gasPriceUrl"]
server = Web3(HTTPProvider(ethConfig["rpcUrl"]))



def getAdmin():
    return server.eth.account.privateKeyToAccount(PRIVATE_KEY)

def getUser(PIN):
    PIN = [int(k) for k in PIN]
    id = userId()
    a = server.solidityKeccak(["bytes16"], [b''])
    b = server.solidityKeccak(["bytes16", "bytes16", "int8"], [a, id, PIN[0]])
    c = server.solidityKeccak(["bytes16", "bytes16", "int8"], [b, id, PIN[1]])
    d = server.solidityKeccak(["bytes16", "bytes16", "int8"], [c, id, PIN[2]])
    pk = server.solidityKeccak(["bytes16", "bytes16", "int8"], [d, id, PIN[3]])
    return server.eth.account.privateKeyToAccount(pk)

def gasPrice():
    try:
        response = requests.get(GAS_URL)
        return int((response.json())["fast"] * 1e9)
    except requests.exceptions.RequestException:
        return int(defaultGasPrice)

def cleanTx(rawReceipt):
    HexBytes = lambda x: x
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

def waitForTx(txHash):
    while True:
        txReceipt = server.eth.getTransactionReceipt(txHash)
        if txReceipt is not None:
            return cleanTx(txReceipt)
        time.sleep(0.5)

def deployContract(flag):
    admin = getAdmin()
    contractData = utilities.binContract(flag)
    rawContract = server.eth.contract(abi=contractData["abi"], bytecode=contractData["bin"])
    gas = rawContract.constructor().estimateGas({"from": admin.address})
    txUnsigned = rawContract.constructor().buildTransaction({
        "from": admin.address,
        "nonce": server.eth.getTransactionCount(admin.address),
        "gas": gas,
        "gasPrice": gasPrice(),
    })
    txSigned = admin.signTransaction(txUnsigned)
    try:
        deploymentHash = server.eth.sendRawTransaction(txSigned.rawTransaction)
    except ValueError:
        print("Insufficent funds for deployment")
        sys.exit(1)
    txReceipt = waitForTx(deploymentHash)
    if txReceipt["status"] == 1:
        contractAddress = txReceipt["contractAddress"]
        contract = server.eth.contract(
            address=contractAddress,
            abi=contractData["abi"],
        )
        startBlock = txReceipt["blockNumber"]
        data = {
            "address": contract.address,
            "startBlock": startBlock
        }
        return data
    else:
        print("Network is down")
        sys.exit(1)

def allDeploy():
    kycData = deployContract("kyc")
    phData = deployContract("ph")
    with open("registrar.json", 'w') as file:
        data = {
        "registrar": kycData,
        "payments": phData
        }
        json.dump(data, file)

def getContract(flag):

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

def invokeContract(sender, methodName, methodArgs, ni=0):

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
    return cleanTx(txHash)

allDeploy()

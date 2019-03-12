from eth_abi import encode_abi
import json
import sys
import time
import requests
from web3 import Web3, HTTPProvider
import utilities

global ethConfig
# global server
ethConfig = utilities.net()
server = Web3(HTTPProvider(ethConfig["rpcUrl"]))

def getAdmin():
    return server.eth.account.privateKeyToAccount(ethConfig["privKey"])

def whoIsAdmin(flag):
    return call(flag, "whoIsOwner")

def getUser(PIN):
    PIN = [int(k) for k in PIN]
    id = utilities.userId()
    a = Web3.solidityKeccak(["bytes16"], [b''])
    b = Web3.solidityKeccak(["bytes16", "bytes16", "int8"], [a, id, PIN[0]])
    c = Web3.solidityKeccak(["bytes16", "bytes16", "int8"], [b, id, PIN[1]])
    d = Web3.solidityKeccak(["bytes16", "bytes16", "int8"], [c, id, PIN[2]])
    pk = Web3.solidityKeccak(["bytes16", "bytes16", "int8"], [d, id, PIN[3]])
    return server.eth.account.privateKeyToAccount(pk)

def gasPrice():
    try:
        response = requests.get(ethConfig["gasPriceUrl"])
        return int((response.json())["fast"] * 1e9)
    except requests.exceptions.RequestException:
        return int(ethConfig["defaultGasPrice"])

def cleanTx(rawReceipt):
    HexBytes = lambda x: x
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

def getReceipt(txHash):
    while True:
        txReceipt = server.eth.getTransactionReceipt(txHash)
        if txReceipt is not None:
            return cleanTx(txReceipt)
        time.sleep(0.5)

def deploy(flag):
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
    txReceipt = getReceipt(deploymentHash)
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
        print("Deployment failed")
        sys.exit(1)

def allDeploy():
    kycData = deploy("kyc")
    phData = deploy("ph")
    with open("registrar.json", 'w') as file:
        data = {
            "registrar": kycData,
            "payments": phData
        }
        json.dump(data, file)

def getContract(flag):
    contractAbi = utilities.binContract(flag)["abi"]
    contractAddress = utilities.getContractAddress(flag)
    contract = server.eth.contract(address=contractAddress, abi=contractAbi)
    return contract

def call(flag, methodName, methodArgs=""):
    contract = getContract(flag)
    args = str(methodArgs)[1:-1]
    rawCall = "contract.functions.{methodName}({methodArgs}).call()".format(methodName=methodName, methodArgs=args)
    return eval(rawCall)

def invoke(flag, sender, methodName, methodArgs, chown=False):
    contract = getContract(flag)
    args = str(methodArgs)[1:-1]
    invoker = "contract.functions.{methodName}({methodArgs})".format(methodName=methodName, methodArgs=args)
    try:
        gas = eval(invoker).estimateGas({"from": sender.address})
        txUnsigned = eval(invoker).buildTransaction({
            "from": sender.address,
            "nonce": server.eth.getTransactionCount(sender.address),
            "gas": gas,
            "gasPrice": gasPrice(),
        })
        txSigned = sender.signTransaction(txUnsigned)
        try:
            txHash = server.eth.sendRawTransaction(txSigned.rawTransaction)
        except ValueError:
            print("An error occured during the invocation")
            sys.exit(1)
        txReceipt = getReceipt(txHash)
        tx = {
            "status": txReceipt["status"],
            "txHash": txReceipt["transactionHash"]
        }
        return tx
    except:
        if chown:
            print("Request cannot be executed")
            sys.exit(1)
        # put other exceptions with flags here
def chown(newOwner):
    if not Web3.isAddress(newOwner):
        print("Invalid address")
        sys.exit(1)
    admin = getAdmin()
    tx = invoke("kyc", admin, methodName="changeOwner", methodArgs=[newOwner], chown=True)
    if tx["status"] != 1:
        print("Transfering ownership failed, but included in {}".format(tx["txHash"]))
        sys.exit(1)

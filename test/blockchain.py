from eth_abi import encode_abi
import json
import sys
import time
import requests
from web3 import Web3, HTTPProvider
import utilities

global ethConfig
global server
ethConfig = utilities.net()
server = Web3(HTTPProvider(ethConfig["rpcUrl"]))

def checkContractValidity(flag):
    suspicionAddress = utilities.getContractAddress(flag)
    utilities.isAddress(suspicionAddress)
    data = utilities.binContract(flag)
    try:
        contract = server.eth.contract(address=suspicionAddress, abi=data["abi"])
        if flag == "kyc":
            contract.functions.validateR().call()
        else:
            contract.functions.validateP().call()
    except:
        print("Seems that the contract address is not the registrar contract")
        sys.exit(1)

def getAdmin():
    return server.eth.account.privateKeyToAccount(ethConfig["privKey"])

def whoIsAdmin(flag):
    return call(flag, "whoIsOwner")

def getUser(PIN):
    utilities.checkPIN(PIN)
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
    AttributeDict = lambda x: x
    return eval(str(rawReceipt)) if rawReceipt is not None else None

def getReceipt(txHash):
    while True:
        txReceipt = server.eth.getTransactionReceipt(txHash)
        if txReceipt is not None:
            return cleanTx(txReceipt)
        time.sleep(0.5)

def deploy(flag):
    admin = getAdmin()
    utilities.isAddress(admin.address)
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
    checkContractValidity(flag)
    contractAbi = utilities.binContract(flag)["abi"]
    contractAddress = utilities.getContractAddress(flag)
    contract = server.eth.contract(address=contractAddress, abi=contractAbi)
    return contract

def isSufficient(user, gas, value=0):
    utilities.isAddress(user.address)
    balance = server.eth.getBalance(user.address)
    return balance >= value + gas * gasPrice()

def call(flag, methodName, methodArgs=[]):
    contract = getContract(flag)
    args = str(methodArgs)[1:-1]
    rawCall = "contract.functions.{methodName}({methodArgs}).call()".format(methodName=methodName, methodArgs=args)
    return eval(rawCall)

def invoke(
    flag,
    sender,
    methodName,
    methodArgs,
    chown=False,
    add=False,
    delt=False,
    confirm=False
):
    utilities.isAddress(sender.address)
    contract = getContract(flag)
    args = str(methodArgs)[1:-1]
    invoker = "contract.functions.{methodName}({methodArgs})".format(methodName=methodName, methodArgs=args)
    try:
        gas = eval(invoker).estimateGas({"from": sender.address})
    except:
        if add:
            print("Delete first")
            sys.exit(1)
        elif chown:
            print("Request cannot be executed")
            sys.exit(1)
        elif delt:
            print("Account is not registered yet")
            sys.exit(1)
        elif confirm:
            print("No funds to send the request")
            sys.exit(1)
    if add or confirm:
        if not isSufficient(sender, gas):
            print("No funds to send the request")
            sys.exit(1)
    # add other exceptions for flags
    txUnsigned = eval(invoker).buildTransaction({
        "from": sender.address,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gas": gas,
        "gasPrice": gasPrice(),
    })
    txSigned = sender.signTransaction(txUnsigned)
    try:
        txHash = server.eth.sendRawTransaction(txSigned.rawTransaction)
    except:
        print("Kahoot")
        sys.exit(1)
    txReceipt = getReceipt(txHash)
    tx = {
        "status": txReceipt["status"],
        "txHash": txReceipt["transactionHash"]
    }
    return tx

def chown(newOwner):
    utilities.isAddress(newOwner)
    admin = getAdmin()
    utilities.isAddress(admin.address)
    tx = invoke("kyc", admin, methodName="changeOwner", methodArgs=[newOwner], chown=True)
    if tx["status"] != 1:
        print("Transfering ownership failed, but included in {}".format(tx["txHash"]))
        sys.exit(1)

def getBalance(PIN):
    user = getUser(PIN)
    utilities.isAddress(user.address)
    return utilities.normalizeValue(server.eth.getBalance(user.address))

def addRequest(PIN, phoneNumber):
    utilities.checkPIN(PIN)
    user = getUser(PIN)
    utilities.isAddress(user.address)
    phoneNumber = utilities.checkAndRefinePhoneNumber(phoneNumber)
    requestStatus = call("kyc", "getStatus", [user.address])
    if requestStatus == 0:
        tx = invoke("kyc", user, "addRequest", [phoneNumber], add=True)
        if tx["status"] == 1:
            return tx["txHash"]
        else:
            print("Failed, but included in {}".format(tx["txHash"]))
            sys.exit(1)
    elif requestStatus == 1:
        print("You have already sent a request for unregistration. Cancel it, and then try again")
        sys.exit(1)
    elif requestStatus > 1:
        print("Registration request already sent")
        sys.exit(1)
    else:
        print("Invalid status")
        sys.exit(1)

def delRequest(PIN):
    utilities.checkPIN(PIN)
    user = getUser(PIN)
    utilities.isAddress(user.address)
    requestStatus = call("kyc", "getStatus", [user.address])
    if requestStatus == 0:
        tx = invoke("kyc", user, "delRequest", [], delt=True)
        if tx["status"] == 1:
            return tx["txHash"]
        else:
            print("Failed, but included in {}".format(tx["txHash"]))
            sys.exit(1)
    elif requestStatus == 1:
        print("Unregistration request already sent")
        sys.exit(1)
    elif requestStatus > 1:
        print("Account is not registered yet")
        sys.exit(1)
    else:
        print("Invalid status")
        sys.exit(1)

def confirmRequest(address):
    utilities.isAddress(address)
    admin = getAdmin()
    utilities.isAddress(admin.address)
    requestStatus = call("kyc", "getStatus", [address])
    if requestStatus != 0:
        tx = invoke("kyc", admin, "confirmRequest", [address], confirm=True)
        if tx["status"] == 1:
            print("Confirmed by {}".format(tx["txHash"]))
            sys.exit(0)
        else:
            print("Failed, but included in {}".format(tx["txHash"]))
            sys.exit(1)
    else:
        print("No requests found")
        sys.exit(0)

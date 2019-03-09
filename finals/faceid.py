#!/usr/bin/env python

import web3
from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse
from eth_account import Account
import cv2
import numpy as np
import os
# import dlib
from random import randrange

# Essentials

def setArgs():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--find',
        type=str,
    )
    parser.add_argument(
        '--actions',
        action='store_true',
    )
    parser.add_argument("--add", action="store", nargs='+', help="Send a request for registration")
    parser.add_argument("--balance", action="store", help="Get the balance of your account")
    parser.add_argument("--del", action="store", help="Delete a request for registration")
    parser.add_argument("--cancel", action="store", help="Cancel any request")
    parser.add_argument("--send", action="store", nargs='+', help="Send money by a phone number")
    args = parser.parse_args()
    return vars(args)

# ---------RUS START---------

class User(object):

    def __init__(self, UUID, PIN):
        self.UUID = "0x" + str(UUID.replace('-', ''))
        self.PIN = [int(k) for k in PIN]

    def setServer(self, server):
        self.server = server

    def generatePrivateKey(self):
        UUID = self.UUID
        PIN = self.PIN
        privateKey = server.solidityKeccak(["bytes16"], [b''])
        for k in range(4):
            privateKey = Web3.solidityKeccak(["bytes16", "bytes16", "int8"], [privateKey, UUID, PIN[k]]) # ABI-packed, keccak256 hashed
        self.privateKey = privateKey

    def generateAddress(self):
        account = Account.privateKeyToAccount(self.privateKey)
        self.address = account.address

def scaleValue(value):
    if value == 0:
        return "0 poa"
    elif value < 1e3:
        return str(value) + " wei"
    elif 1e3 <= value < 1e6:
        val = float("{:.6f}".format((float(value) / 1e3)))
        return str(int(val)) + " kwei" if val - int(val) == 0 else str(val) + " kwei"
    elif 1e6 <= value < 1e9:
        val = float("{:.6f}".format((float(value) / 1e6)))
        return str(int(val)) + " mwei" if val - int(val) == 0 else str(val) + " mwei"
    elif 1e9 <= value < 1e12:
        val = float("{:.6f}".format((float(value) / 1e9)))
        return str(int(val)) + " gwei" if val - int(val) == 0 else str(val) + " gwei"
    elif 1e12 <= value < 1e15:
        val = float("{:.6f}".format((float(value) / 1e12)))
        return str(int(val)) + " szabo" if val - int(val) == 0 else str(val) + " szabo"
    elif 1e15 <= value < 1e18:
        val = float("{:.6f}".format((float(value) / 1e15)))
        return str(int(val)) + " finney" if val - int(val) == 0 else str(val) + " finney"
    else:
        val = float("{:.6f}".format((float(value) / 1e18)))
        return str(int(val)) + " poa" if val - int(val) == 0 else str(val) + " poa"

def getBalanceByID(server):
    try:
        with open("person.json", 'r') as person:
            data = json.load(person)
            id = str(data["id"])
        PIN = args["balance"]
        user = User(id, PIN)
        user.setServer(server)
        user.generatePrivateKey()
        user.generateAddress()
        balance = scaleValue(server.eth.getBalance(user.address))
        print("Your balance is {}".format(balance))
    except:
        print("ID is not found")

def getUser(server, privateKey):
    return server.eth.account.privateKeyToAccount(privateKey)

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
    return _bytecode, _abi

def phData():
    with open("PaymentHandler.bin", 'r') as bin:
        _bytecode = bin.read()
    with open("PaymentHandler.abi", 'r') as abi:
        _abi = json.loads(abi.read())
    return _bytecode, _abi

def send(server, sender, dest, val):
    txUnsigned = {
        "from": sender.address,
        "to": dest,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gas": 21000,
        "gasPrice": getGasPrice(speed="fast"),
        "value": int(val),
    }
    txSigned = sender.signTransaction(txUnsigned)
    try:
        txHash = server.eth.sendRawTransaction(txSigned.rawTransaction).hex()
    except:
        return "No funds to send the payment"
    return txHash

def getContract(server, flag):

    try:
        with open("registrar.json", 'r') as db:
            data = json.load(db)
    except:
        return "No contract address"
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

# ---------------------------

def addRequest(server, user, phoneNumber):
    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    _user = getUser(server, user.privateKey)

    if server.eth.getBalance(_user.address) <= 0:
        return "No funds to send the request"

    status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
    if status == 0:
        txHash = invokeContract(server, _user, _contract, methodName="addRequest", methodArgs=[phoneNumber])
        return "Registration request sent by {}".format(txHash)
    elif status > 1:
        return "Registration request already sent"
    elif status == 1:
        return "Unregistration request already sent. SWW"

def delRequest(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract

    _user = getUser(server, user.privateKey)
    if server.eth.getBalance(_user.address) <= 0:
        return "No funds to send the request"

    status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
    if status == 1:
        return "Unregistration request already sent"
    elif status == 0:
        return "There are no registration requests"
    elif status == 1:
        try:
            txHash = invokeContract(server, _user, _contract, methodName="delRequest", methodArgs=[])
            return "Unregistration request sent by {}".format(txHash)
        except:
            return "Account is not registered yet"
    else:
        return "Account is not registered yet"
#
# def cancelRequest(server, user):
#
#     _contract = getContract(server, flag="kyc")
#     if _contract == "No contract address":
#         return _contract
#     try:
#         callContract(_contract, methodName="watermark", methodArgs=[])
#         _user = getUser(server, user.privateKey)
#         if server.eth.getBalance(user.address) <= 0:
#             return "No funds to send the request"
#         status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
#         if status == 0:
#             return "No requests found"
#         elif status == 1:
#             try:
#                 txHash = invokeContract(server, _user, _contract, methodName="cancelRequest", methodArgs=[])
#                 return "Unregistration canceled by {}".format(txHash)
#             except:
#                 return "Account is not registered yet"
#         elif status > 1:
#             if server.eth.getBalance(user.address) <= 0:
#                 return "No funds to send the request"
#             else:
#                 try:
#                     txHash = invokeContract(server, _user, _contract, methodName="cancelRequest", methodArgs=[])
#                     return "Registration canceled by {}".format(txHash)
#                 except:
#                     return "Account is not registered yet"
#     except:
#         return "Seems that the contract address is not the registrar contract"

# def sendByNumber(server, user, pn, val):
#     _contract = getContract(server, flag="kyc")
#     if _contract == "No contract address":
#         return _contract
#     if not isContract(_contract):
#         return "Seems that the contract address is not the registrar contract"
#     _user = getUser(server, user.privateKey)
#     refinedNumber = int(str(pn)[1:])
#     destAddress = invokeContract(server, _user, _contract, methodName="getAddressByNumber", methodArgs=[refinedNumber])
#     if destAddress == 0:
#         print("No account with the phone number {}".format(pn))
#     elif (server.isAddress(destAddress)):
#         txHash = send(server, _user, destAddress, val)
#         if txHash == "No funds to send the payment":
#             print(txHash)
#         print("Payment of {a} to {d} scheduled".format(a=scaleValue(int(val)), d=pn))
#         print("Transaction Hash: {}".format(txHash))
#     else:
#         raise ValueError

# ----------RUS END----------

# ---------MAG START---------


def GetKey():
    with open('faceapi.json') as f:
        privateKey = eval(f.read())['key']
    return privateKey

def GetGroupId():
    with open('faceapi.json') as f:
        groupId = eval(f.read())['groupId']
    return groupId

def GetBaseUrl():
    with open('faceapi.json') as f:
        serviceUrl = eval(f.read())['serviceUrl']
    return serviceUrl

def MakeDetectRequest(buf):
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'returnFaceId': True,
        'returnFaceRectangle': False,
    }
    baseUrl = GetBaseUrl() + 'detect/'
    req = requests.post(
        baseUrl,
        params=params,
        headers=headers,
        data=buf,
    )
    return req.json()

def GetOctetStream(image):
    ret, buf = cv2.imencode('.jpg', image)
    return buf.tobytes()

def Detect(videoFrames):
    result = []
    for frame in videoFrames:
        image = GetOctetStream(frame)
        req = MakeDetectRequest(image)
        if (len(req) != 0):
            result.append(req[0]['faceId'])
    return result

def Identify(videoFrames):
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    ids = Detect(videoFrames)
    data = {
        'faceIds': ids,
        'personGroupId': GetGroupId(),
    }
    baseUrl = GetBaseUrl() + '/identify'
    req = requests.post(
        baseUrl,
        headers=headers,
        json=data,
    )
    return req.json()

def GetVideoFrames(videoName):
    vcap = cv2.VideoCapture(videoName)
    result = []
    frames = []
    while (True):
        ret, frame = vcap.read()
        if (frame is None):
            break
        else:
            frames.append(frame)
    if (len(frames) < 5):
        return result
    for i in range(0, len(frames), len(frames) // 4):
        if (len(result) == 4 or len(frames) < 5):
            break
        result.append(frames[i])
    result.append(frames[-1])
    vcap.release()
    return result

def GetTrainingStatus():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    params = {
        'personGroupId': GetGroupId(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/training'
    req = requests.get(
        baseUrl,
        params=params,
        headers=headers,
    )
    return req.json()

def GetList():
    headers = {
        'Ocp-Apim-Subscription-Key': GetKey(),
    }
    baseUrl = GetBaseUrl() + 'persongroups/' + GetGroupId() + '/persons'
    req = requests.get(
        baseUrl,
        headers=headers,
    )
    return req

def CreateFile(id):
    f = open('person.json', 'w')
    f.write('{"id": "' + id + '"}')
    f.close()

def DeleteFile():
    if (os.path.isfile('person.json')):
        os.remove('person.json')

def GetPersonsData():
    req = GetList()
    if (str(req) == '<Response [200]>'):
        req = GetList().json()
        persons = []
        for person in req:
            persons.append({
                'personId':person['personId'],
                'name':person['name'],
                'userData':person['userData']
            })
        return persons
    else:
        return 'The group does not exist'

def Find(videoName):
    videoFrames = GetVideoFrames(videoName)
    persons = GetPersonsData()
    if (len(videoFrames) < 5):
        print('The video does not follow requirements')
        DeleteFile()
        return None
    if (persons == 'The group does not exist'):
        print('The service is not ready')
        DeleteFile()
        return None
    f = 1
    for person in persons:
        if (person['userData'] != 'trained'):
            f = 0
    if (f == 0):
        print('The service is not ready')
        DeleteFile()
        return None
    else:
        result = Identify(videoFrames)
        if (len(result) < 5):
            print('The video does not follow requirements')
            DeleteFile()
            return None
        candidates = dict()
        for frame in result:
            for candidate in frame['candidates']:
                currPersonId = candidate['personId']
                currConfidence = candidate['confidence']
                if (candidates.get(currPersonId) == None):
                    if (currConfidence >= 0.5):
                        candidates[currPersonId] = currConfidence
                else:
                    if (currConfidence >= 0.5):
                        candidates[currPersonId] += currConfidence
                    else:
                        candidates[currPersonId] = -100000
        if (len(candidates) == 0):
            print('The person was not found')
            DeleteFile()
            return None
        maxConfidence = 0
        bestCandidate = ''
        for candidate, confidence in candidates.items():
            if (confidence >= 2.5):
                if (maxConfidence < confidence):
                    bestCandidate = candidate
                    maxConfidence = confidence
        if (maxConfidence < 2.5):
            print('The person was not found')
            DeleteFile()
            return None
        else:
            print(bestCandidate + ' identified')
            CreateFile(bestCandidate)
            return None

def SetActions():
    f = open('actions.json', 'w')
    actions = [
        'yaw right',
        'yaw left',
        'roll right',
        'roll left',
        'close right eye',
        'close left eye',
        'open mouth',
    ]
    ans = ''
    for i in range(7):
        rand = randrange(len(actions))
        ans += actions[rand] + '\n'
        actions.remove(actions[rand])
    f.write(ans)
    f.close()

# ----------MAG END-----------

# ---------MAIN MUTEX---------

if __name__ == "__main__":

    # ----------START SET------------

    with open("network.json", 'r') as ethConfig:
        global _defaultGasPrice
        global _gasPriceURL
        global _rpcURL
        read = json.load(ethConfig)
        _rpcURL = str(read["rpcUrl"])
        _gasPriceURL = str(read["gasPriceUrl"])
        _defaultGasPrice = str(read["defaultGasPrice"])

    args = setArgs()
    server = Web3(HTTPProvider(_rpcURL))

    # -----------END SET-------------

    # ------ACCEPTANCE ZONE START----

    if args["balance"] is not None:
        getBalanceByID(server)

    # ------ACCEPTANCE ZONE START----

    elif args["add"] is not None:

        try:
            with open("person.json", 'r') as person:
                _UUID = str(json.load(person)["id"])
            _phoneNumber = args["add"][1]
            if _phoneNumber[0] == '+' and _phoneNumber[1:].isdigit() and len(_phoneNumber) == 12:
                _PIN = args["add"][0]
                user = User(_UUID, _PIN)
                user.generatePrivateKey()
                user.generateAddress()
                print(addRequest(server, user, int(_phoneNumber[1:])))
            else:
                print("Incorrect phone number")

        except:
            print("ID is not found")

    # US-015
    elif args["del"] is not None:
        try:
            with open("person.json", 'r') as person:
                _UUID = str(json.load(person)["id"])
            _PIN = args["del"]
            user = User(_UUID, _PIN)
            user.generatePrivateKey()
            user.generateAddress()
            print(delRequest(server, user))
        except:
            print("ID is not found")

    # US-016
    elif args["cancel"] is not None:
        try:
            with open("person.json", 'r') as person:
                _UUID = str(json.load(person)["id"])
            _PIN = args["cancel"]
            user = User(_UUID, _PIN)
            user.generatePrivateKey()
            user.generateAddress()
            print(cancelRequest(server, user))
        except:
            print("ID is not found")

    # US-017
    elif args["send"] is not None:
        try:
            with open("person.json", 'r') as person:
                _UUID = str(json.load(person)["id"])
            _PIN = args["send"][0]
            _phoneNumber = args["send"][1]
            if len(str(_phoneNumber)) != 11:
                print("Incorrect phone number")
            else:
                _value = args["send"][2]
                user = User(_UUID, _PIN)
                user.generatePrivateKey()
                user.generateAddress()
                sendByNumber(server, user, _phoneNumber, _value)
        except:
            print("ID is not found")

    elif (args['find'] != None):
        Find(args['find'])

    elif (args['actions'] == True):
        SetActions()

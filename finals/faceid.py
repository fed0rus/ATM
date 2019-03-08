#!/usr/bin/env python

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

def isContract(contract):
    stub, abi = kycData()
    return contract.abi == abi

# ---------------------------

def addRequest(server, user, phoneNumber):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract
    if not isContract(_contract):
        return "Seems that the contract address is not the registrar contract"
    _user = getUser(server, user.privateKey)
    status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
    if status == 0:
        if server.eth.getBalance(user.address) <= 0:
            return "No funds to send the request"
        else:
            txHash = invokeContract(server, _user, _contract, methodName="addRequest", methodArgs=[phoneNumber])
            return "Registration request sent by {}".format(txHash)
    elif status > 1:
        return "Registration request already sent"

def delRequest(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract
    if not isContract(_contract):
        return "Seems that the contract address is not the registrar contract"
    _user = getUser(server, user.privateKey)
    status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
    if status == 1:
        return "Unregistration request already sent"
    elif status > 1:
        if server.eth.getBalance(user.address) <= 0:
            return "No funds to send the request"
        else:
            try:
                txHash = invokeContract(server, _user, _contract, methodName="delRequest", methodArgs=[])
                return "Registration request sent by {}".format(txHash)
            except:
                return "Account is not registered yet"
    else:
        return "Account is not registered yet"

def cancelRequest(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract
    if not isContract(_contract):
        return "Seems that the contract address is not the registrar contract"
    _user = getUser(server, user.privateKey)
    if server.eth.getBalance(user.address) <= 0:
        return "No funds to send the request"
    status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
    if status == 0:
        return "No requests found"
    elif status == 1:
        try:
            txHash = invokeContract(server, _user, _contract, methodName="cancelRequest", methodArgs=[])
            return "Unregistration canceled by {}".format(txHash)
        except:
            return "Account is not registered yet"
    elif status > 1:
        if server.eth.getBalance(user.address) <= 0:
            return "No funds to send the request"
        else:
            try:
                txHash = invokeContract(server, _user, _contract, methodName="cancelRequest", methodArgs=[])
                return "Registration canceled by {}".format(txHash)
            except:
                return "Account is not registered yet"

def sendByNumber(server, user, pn, val):
    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract
    if not isContract(_contract):
        return "Seems that the contract address is not the registrar contract"
    _user = getUser(server, user.privateKey)
    refinedNumber = int(str(pn)[1:])
    destAddress = invokeContract(server, _user, _contract, methodName="getAddressByNumber", methodArgs=[refinedNumber])
    if destAddress == 0:
        print("No account with the phone number {}".format(pn))
    elif (server.isAddress(destAddress)):
        txHash = send(server, _user, destAddress, val)
        if txHash == "No funds to send the payment":
            print(txHash)
        print("Payment of {a} to {d} scheduled".format(a=scaleValue(int(val)), d=pn))
        print("Transaction Hash: {}".format(txHash))
    else:
        raise ValueError

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
        global _privateKey
        read = json.load(ethConfig)
        _rpcURL = str(read["rpcUrl"])
        _privateKey = str(read["privKey"])
        _gasPriceURL = str(read["gasPriceUrl"])
        _defaultGasPrice = str(read["defaultGasPrice"])

    args = setArgs()
    server = Web3(HTTPProvider(_rpcURL))

    # -----------END SET-------------

    # US-013
    if args["balance"] is not None:
        getBalanceByID(server)

    # US-014
    elif args["add"] is not None:
        try:
            with open("person.json", 'r') as person:
                _UUID = str(json.load(person)["id"])
        except:
            print("ID is not found")

        _phoneNumber = args["add"][1]
        if _phoneNumber[0] == '+' and _phoneNumber[1:].isdigit() and len(_phoneNumber) == 12:
            _PIN = args["add"][0]
            user = User(_UUID, _PIN)
            user.generatePrivateKey()
            user.generateAddress()
            print(addRequest(server, user, int(_phoneNumber[1:])))
        else:
            print("Incorrect phone number")

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

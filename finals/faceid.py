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
import dlib
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
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a031916331790556107418061003e6000396000f3fe6080604052600436106100fa576000357c010000000000000000000000000000000000000000000000000000000090048063851b16f51161009c578063de1d544f11610076578063de1d544f1461029e578063e5b18630146102c8578063e9238cc4146102fb578063f13dc2e214610325576100fa565b8063851b16f5146102415780639ee1bd0f14610256578063a6f9dae11461026b576100fa565b80634ca1fad8116100d85780634ca1fad8146101ba5780635a58cd4c146101e457806374adad1d146101f957806383904f8d1461022c576100fa565b806309e6707d146100fc5780631d25899b1461014157806330ccebb514610187575b005b34801561010857600080fd5b5061012f6004803603602081101561011f57600080fd5b5035600160a060020a031661034e565b60408051918252519081900360200190f35b34801561014d57600080fd5b5061016b6004803603602081101561016457600080fd5b5035610360565b60408051600160a060020a039092168252519081900360200190f35b34801561019357600080fd5b5061012f600480360360208110156101aa57600080fd5b5035600160a060020a031661037b565b3480156101c657600080fd5b506100fa600480360360208110156101dd57600080fd5b5035610396565b3480156101f057600080fd5b506100fa610468565b34801561020557600080fd5b5061012f6004803603602081101561021c57600080fd5b5035600160a060020a031661048d565b34801561023857600080fd5b506100fa61049f565b34801561024d57600080fd5b506100fa610551565b34801561026257600080fd5b5061016b610657565b34801561027757600080fd5b506100fa6004803603602081101561028e57600080fd5b5035600160a060020a0316610666565b3480156102aa57600080fd5b5061016b600480360360208110156102c157600080fd5b50356106c7565b3480156102d457600080fd5b5061012f600480360360208110156102eb57600080fd5b5035600160a060020a03166106ef565b34801561030757600080fd5b5061016b6004803603602081101561031e57600080fd5b503561070a565b34801561033157600080fd5b5061033a610710565b604080519115158252519081900360200190f35b60026020526000908152604090205481565b600160205260009081526040902054600160a060020a031681565b600160a060020a031660009081526003602052604090205490565b3315156103a257600080fd5b6402540be40081101580156103bc575064174876e7ff8111155b15156103c757600080fd5b33600090815260036020526040902054156103e157600080fd5b60048054600181019091557f8a35acfbc15ff81a39ae7d344fd709f28e8600b4aa8c65c6b64bfe7fe36bd19b01805473ffffffffffffffffffffffffffffffffffffffff191633908117909155600081815260036020526040808220849055517fdc79fc57451962cfe3916e686997a49229af75ce2055deb4c0f0fdf3d5d2e7c19190a250565b600054600160a060020a0316331461047f57600080fd5b600054600160a060020a0316ff5b60036020526000908152604090205481565b3315156104ab57600080fd5b336000908152600260205260409020546001106104c757600080fd5b6004805460018181019092557f8a35acfbc15ff81a39ae7d344fd709f28e8600b4aa8c65c6b64bfe7fe36bd19b01805473ffffffffffffffffffffffffffffffffffffffff19163390811790915560008181526003602052604080822093909355915190917f64ed2364f9ee0643b60aeffba4ace8805648fad0d546c5efd449d1de10c8dcee91a2565b33151561055d57600080fd5b33600090815260036020526040902054151561057857600080fd5b3360009081526003602052604081205460011415610594575060015b3360008181526003602052604081208190556004805460018101825591527f8a35acfbc15ff81a39ae7d344fd709f28e8600b4aa8c65c6b64bfe7fe36bd19b01805473ffffffffffffffffffffffffffffffffffffffff1916909117905580156106285760405133907f8c08d387d1333f3da7e980dd7fc958615d513ca73155b6dd2a5a13e17acd116290600090a2610654565b60405133907fffdf549003cf56ac2e863a28d8d5191467cf2a6d5e659f6a649e855a3d8cd8d090600090a25b50565b600054600160a060020a031690565b600054600160a060020a0316331461067d57600080fd5b600054600160a060020a038281169116141561069857600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a0392909216919091179055565b60048054829081106106d557fe5b600091825260209091200154600160a060020a0316905081565b600160a060020a031660009081526002602052604090205490565b50600090565b60019056fea165627a7a72305820220ba6ea1381f37aee9b2534baecd4d41c58b90eb5b5e8739d895be1464f5b930029"
    _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getStatus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_phoneNumber","type":"uint256"}],"name":"addRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"requests","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"cancelRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"bulkLog","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getNumberByAddress","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_number","type":"uint256"}],"name":"getAddressByNumber","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"watermark","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"pure","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationCanceled","type":"event"}]')
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

# ---------------------------

def addRequest(server, user, phoneNumber):
    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract
    try:
        callContract(_contract, methodName="watermark", methodArgs=[])
        _user = getUser(server, user.privateKey)
        if server.eth.getBalance(_user.address) <= 0:
            return "No funds to send the request"
        status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
        if status <= 1:
            txHash = invokeContract(server, _user, _contract, methodName="addRequest", methodArgs=[phoneNumber])
            return "Registration request sent by {}".format(txHash)
        elif status > 1:
            return "Registration request already sent"
    except:
        return "Seems that the contract address is not the registrar contract"

def delRequest(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract
    try:
        callContract(_contract, methodName="watermark", methodArgs=[])
        _user = getUser(server, user.privateKey)
        if server.eth.getBalance(_user.address) <= 0:
            return "No funds to send the request"
        status = callContract(_contract, methodName="getStatus", methodArgs=[user.address])
        if status == 1:
            return "Unregistration request already sent"
        elif status > 1:
            try:
                txHash = invokeContract(server, _user, _contract, methodName="delRequest", methodArgs=[])
                return "Unregistration request sent by {}".format(txHash)
            except:
                return "Account is not registered yet"
        else:
            return "Account is not registered yet"
    except:
        return "Seems that the contract address is not the registrar contract"

def cancelRequest(server, user):

    _contract = getContract(server, flag="kyc")
    if _contract == "No contract address":
        return _contract
    try:
        callContract(_contract, methodName="watermark", methodArgs=[])
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
    except:
        return "Seems that the contract address is not the registrar contract"

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

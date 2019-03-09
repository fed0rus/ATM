#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse

# -----------UTILS START------------

HexBytes = lambda x: x

def initParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("--owner", action="store", help="Know the owner of the contract")
    parser.add_argument("--chown", action="store", nargs='+', help="Change the owner of the contract")
    parser.add_argument("--send", action="store", nargs='+', help="Send money")
    args = parser.parse_args()
    return vars(args)

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

def deployContract(server, owner, flag):
    # switch contract type
    if flag == "kyc":
        _bytecode, _abi = kycData()
    elif flag == "ph":
        _bytecode, _abi = phData()
    # deployment
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
        return contract.address, startBlock
    else:
        raise

def getContract(server, flag):

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

# -----------UTILS END------------

# ---------ESSENTIALS START---------

def deploy(server, owner):

    KYCAddress, sb1 = deployContract(server, owner, flag="kyc")
    PHAddress, sb2 = deployContract(server, owner, flag="ph")
    data = {
        "registrar": {
            "address": KYCAddress,
            "startBlock": sb1
        },
        "payments": {
            "address": PHAddress,
            "startBlock": sb2
        }
    }
    with open("registrar.json", 'w') as db:
        json.dump(data, db)
    print("KYC Registrar: {}".format(KYCAddress))
    print("Payment Handler: {}".format(PHAddress))

def returnOwner(server, flag):

    _contract = getContract(server, flag)
    ownerAddress = callContract(_contract, methodName="whoIsOwner")
    return ownerAddress

def changeOwner(server, owner, newOwner, flag):
    assert server.isAddress(newOwner), "SWW"
    _contract = getContract(server, flag)
    txHash = invokeContract(server, owner, _contract, methodName="changeOwner", methodArgs=[newOwner])

# ---------ESSENTIALS END---------


# ----------MAIN MUTEX------------

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

    args = initParser()
    server = Web3(HTTPProvider(_rpcURL))
    user = getUser(server, _privateKey)

    # -----------END SET-------------

    # US-001
    if args["deploy"] is not False:
        deploy(server, user)

    # US-002
    elif args["owner"] is not None:
        if args["owner"] == "registrar":
            ownerAddress = returnOwner(server, flag="kyc")
            print("Admin account: {}".format(ownerAddress))
        elif args["owner"] == "payments":
            ownerAddress = returnOwner(server, flag="ph")
            print("Admin account: {}".format(ownerAddress))
        else:
            raise ValueError("Enter a valid contract type")

    # US-003
    elif args["chown"] is not None:

        if args["chown"][0] == "registrar":
            try:
                newAdminAccount = args["chown"][1]
                changeOwner(server, user, newOwner=newAdminAccount, flag="kyc")
                print("New admin account: {}".format(newAdminAccount))
            except:
                print("Request cannot be executed")
        elif args["chown"][0] == "payments":
            try:
                newAdminAccount = args["chown"][1]
                changeOwner(server, user, newOwner=newAdminAccount, flag="ph")
                print("New admin account: {}".format(newAdminAccount))
            except:
                print("Request cannot be executed")
        else:
            raise ValueError("Enter a valid contract type")

'''
compile:
    solc --abi --bin --optimize --overwrite -o ./ KYCRegistrar.sol && solc --abi --bin --optimize --overwrite -o ./ PaymentHandler.sol
'''

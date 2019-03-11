#!/usr/bin/env python

import blockchain
import arguments

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

if __name__ == "__main__":

    # ----------START SET------------
    ethConfig = utilities.getFile("network.json")
    if ethConfig == -1:


    args = arguments.getArgs()
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

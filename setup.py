import utilities
import blockchain

args = utilities.getArgs()

if __name__ == "__main__":

    if args["deploy"] == True:
        blockchain.allDeploy()
        registrarAddress = utilities.getContractAddress("kyc")
        handlerAddress = utilities.getContractAddress("ph")
        print("KYC Registrar: {}\nPayment Handler: {}".format(registrarAddress, handlerAddress))

    elif args["owner"] is not None:
        admin = blockchain.whoIsAdmin("kyc")
        print("Admin account: {}".format(admin))

    elif args["chown"] is not None:
        newOwner = args["chown"][1]
        blockchain.chown(newOwner)
        print("New admin account: {}".format(newOwner))

    elif args["test"] == True:
        pass

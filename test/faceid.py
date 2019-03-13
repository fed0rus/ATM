import utilities
import blockchain
import sys

args = utilities.getArgs()

if __name__ == "__main__":

    if args["balance"] is not None:
        PIN = args["balance"]
        balance = blockchain.getBalance(PIN)
        print("Your balance is {}".format(balance))

    elif args["add"] is not None:
        PIN = args["add"][0]
        phoneNumber = args["add"][1]
        txHash = blockchain.addRequest(PIN, phoneNumber)
        print("Registration request sent by {}".format(txHash))

    elif args["del"] is not None:
        PIN = args["del"]
        txHash = blockchain.delRequest(PIN)
        print("Unregistration request sent by {}".format(txHash))

    elif args["test"] == True:
        pass

import utilities
import blockchain
import sys

args = utilities.getArgs()

if __name__ == "__main__":

    if args["balance"] is not None:
        PIN = args["balance"][0]
        balance = blockchain.getBalance(PIN)
        print("Your balance is {}".format(balance))

    elif args["add"] is not None:
        PIN = args["add"][0]
        phoneNumber = args["add"][1]
        txHash = blockchain.addRequest(PIN, phoneNumber)
        print("Registration request sent by {}".format(txHash))

    elif args["test"] == True:
        pass

import utilities
import blockchain

args = utilities.getArgs()

if __name__ == "__main__":

    if args["balance"] is not None:
        PIN = args["balance"]
        balance = blockchain.getBalance(PIN)
        print("Your balance is {}".format(balance))

    elif args["add"] is not None:
        phoneNumber = args["add"][0]
        PIN = args["add"][1]
        txHash = blockchain.add(PIN, phoneNumber)
        print("Registration request sent by {}".format(txHash))

    elif args["test"] == True:
        pass

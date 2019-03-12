import utilities
import blockchain

args = utilities.getArgs()

if __name__ == "__main__":

    if args["balance"] is not None:
        PIN = args["balance"]
        balance = blockchain.getBalance(PIN)
        print("Your balance is {}".format(balance))

    elif args["add"] is not None:
        

    elif args["test"] == True:
        pass

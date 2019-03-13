import utilities
import blockchain
import sys

args = utilities.getArgs()

if __name__ == "__main__":

    if args["confirm"] is not None:
        address = args["confirm"]
        blockchain.confirmRequest(address)

    elif args["test"] == True:
        pass

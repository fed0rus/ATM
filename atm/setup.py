import utilities
import blockchain
import arguments

args = arguments.getArgs()

if __name__ == "__main__":

    if args["deploy"] == True:
        blockchain.allDeploy()

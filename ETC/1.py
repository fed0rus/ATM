from web3 import Web3, HTTPProvider
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key", help="Private key")
args = parser.parse_args()


server = Web3(HTTPProvider("https://sokol.poa.network"))

privateKey = bytes.fromhex(args.key)

userAddress = server.personal.importRawKey(privateKey, '')

print(userAddress)

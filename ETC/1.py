from web3 import Web3, HTTPProvider
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-k", "--key", help="Private key")
args = parser.parse_args()


server = Web3(HTTPProvider("https://sokol.poa.network"))

privateKey = bytes.fromhex(input("Private key: "))

userAddress = server.personal.importRawKey(privateKey, '')

<<<<<<< HEAD
print()
=======
print(userAddress)
>>>>>>> d33e2a39c6ece9d4aecedd84b146af2ef8eda0f5

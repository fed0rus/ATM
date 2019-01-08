from web3 import Web3

class User(object):
    def __init__(self, UUID, PIN):
        self.UUID = str(UUID)
        self.PIN = str(PIN)

    def extractPIN(self):
        return [int(k) for k in self.PIN]

    def extractUUID(self):
        return (self.UUID).replace('-', '')

    def generatePrivateKey(self): # UUID <- str ... PIN <- [int]
        UUID = self.extractUUID()
        PIN = self.extractPIN()
        privateKey = Web3.soliditySha3(["bytes16"], [b''])
        for k in range(4):
            privateKey = Web3.soliditySha3(["bytes16", "bytes16", "int8[]"], [privateKey, bytearray.fromhex(UUID), [PIN[k]]]) # add abi.encodePacked()
        self.privateKey = privateKey

uuid = input()
pin = input()
user = User(uuid, pin)
user.generatePrivateKey()
print(user.privateKey)

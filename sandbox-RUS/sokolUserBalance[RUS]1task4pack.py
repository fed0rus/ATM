import web3
from web3.auto import w3

class User(object):
    def __init__(self, UUID, PIN):
        self.UUID = str(UUID)
        self.PIN = str(PIN)

    def extractPin(self):
        return [int(k) for k in self.PIN]

    def extractUUID(self):
        return (self.UUID).replace('-', '')

    def generatePrivateKey(self): # UUID <- str ... PIN <- [int]
        UUID = self.extractedUUID()
        PIN = self.extractPIN()
        privateKey = web3.utils.soliditySha3('')
        for k in range(4):
            privateKey = web3.utils.soliditySha3(privateKey, UUID, PIN[k]) # add abi.encodePacked()
        self.privateKey = privateKey

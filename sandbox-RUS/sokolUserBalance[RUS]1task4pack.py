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
        privateKey = keccak256('')
        for k in range(4):
            privateKey = keccak256(privateKey, UUID, PIN[k]) # add abi.encodePacked()
        return str(privateKey)

class Key(object):
    def __init__(self, extractedUUID, extractedPIN):
        self.privateKey = generatePrivateKey(extractUUID, extractedPIN)
# web3 !!!

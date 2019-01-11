import web3
from web3 import Web3, HTTPProvider
server = Web3(HTTPProvider("https://sokol.poa.network/"))

def AttributeDict(self):
    return self

def HexBytes(self):
    return self

def filteredTX(self):
    return eval(str(self))

file = open("eventLogs.txt", 'r')
eventLogs = ''
for i in file:
    eventLogs += i.strip() + '\n'
eventLogs = eval(eventLogs)
file.close()

trans = {}
i = 0
for event in eventLogs:
    if event['args']['tx_source'] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
        i += 1
        print(i + 1)
        account = event['args']['recipient']
        tx = filteredTX(server.eth.getTransaction(event['transactionHash']))
        trans[account] = "master_" + str(tx['blockNumber'])
print(trans)

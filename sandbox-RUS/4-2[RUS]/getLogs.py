import web3
from web3 import Web3, HTTPProvider

# Stubs for eval()

def AttributeDict(self):
    return self

def HexBytes(self):
    return self

server = Web3(HTTPProvider("https://sokol.poa.network/"))

contractAddress = server.toChecksumAddress("0x119041553c1d9f7d0D6Af5B7A0954B2591d8C2dC")
contractABI = [{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"deleteContract","inputs":[],"constant":False},{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"gSS","inputs":[],"constant":False},{"type":"event","name":"AddName","inputs":[{"type":"string","name":"name","indexed":False}],"anonymous":False}]
contract = server.eth.contract(address=contractAddress, abi=contractABI)

eventFilter = contract.events.AddName.createFilter(fromBlock=0, toBlock='latest')
log = eventFilter.get_all_entries()

for index in range(len(log)):
    log[index] = eval(str(log[index]))

eventLog = open("eventLog.txt", "w+")
eventLog.flush()
for event in log:
    eventLog.write(str(event) + ",\n")

eventLog.close()
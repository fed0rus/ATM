import web3
from web3 import Web3, HTTPProvider
server = Web3(HTTPProvider("https://sokol.poa.network/"))

allRootBlocks = [6071558, 6070919, 6071689, 6071818, 6071307, 6071058, 6071188, 6071576, 6070939, 6071837, 6071457, 6071333, 6071081, 6070959, 6071731, 6071098, 6071227, 6071356, 6070845, 6071484, 6071617, 6071750, 6071111, 6070864, 6070993, 6071248, 6071505, 6071386, 6071136, 6071779, 6070884, 6071270, 6071526, 6071016, 6071284, 6070901, 6071669, 6071796, 6071161, 6071419]

userAddress = input("Your address: ")
file = open("eventLogs.txt", 'r')
eventLogs = ''
for i in file:
    eventLogs += i.strip() + '\n'
eventLogs = eval(eventLogs)
file.close()

used = {} # key is address,
global blocks
blocks = []

answer = []
poolFile = open("pool.txt", 'r')
trans = eval(poolFile.read())
poolFile.close()
i = 0
def dfs(used, current): # current = node address
    global i
    used[current] = 1
    senders = []
    print('in')
    f = 0
    for sender in trans[current]:
        f = 1
        if used.get(sender) == None:
            i += 1
            print(i)
            dfs(used, sender)
    if f == 0:
        for event in eventLogs:
            if event['args']['tx_source'] == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                if event['args']['recipient'] == current:
                    tx = filteredTX(server.eth.getTransaction(event['transactionHash']))
                    answer.append(tx['blockNumber'])

dfs(used, userAddress)
print(answer)

userAddress = input("User address: ")
print("Preparing data...")
log = open("eventLog.txt", 'r')
masterLog = eval(log.read())
log.close()

blocks = []
print("Extracting data...")
for k in range(len(masterLog)):
    print("Processing " + str(k))
    txReceipt = masterLog[k]
    if txReceipt['args']['recipient'] == userAddress and txReceipt['args']['value'] >= 0:
        blocks.append(txReceipt['blockNumber'])
        print("-------------------------------")
        print("-------------------------------")
        print("Found a record on " + str(k) + " with BN " + str(txReceipt['blockNumber']))
        print("-------------------------------")
        print("-------------------------------")

print(blocks)
print(set(blocks))

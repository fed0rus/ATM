userAddress = input("Your address: ")

file = open("eventLogs.txt", 'r')
eventLogs = ''
for i in file:
    eventLogs += i.strip() + '\n'
eventLogs = eval(eventLogs)
file.close()

poolFile = open("newPool.txt", 'r')
trans = eval(poolFile.read())
poolFile.close()

answer = list()
used = {}
i = 0
def dfs(used, current, answer): # current = node address
        global i
        used[current] = 1
        print('in')
        for sender in trans[current]:
            if 'm' in sender:
                answer.append(sender)
                print("---------------------------")
                print("FOUND MASTER AT " + sender)
                print("---------------------------")
            elif used.get(sender) == None:
                i += 1
                print(i)
                dfs(used, sender, answer)

dfs(used, userAddress, answer)

print(answer)

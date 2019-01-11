userAddress = input("Your address: ")

file = open("eventLogs.txt", 'r')
eventLogs = ''
for i in file:
    eventLogs += i.strip() + '\n'
eventLogs = eval(eventLogs)
file.close()

poolFile = open("pool.txt", 'r')
trans = eval(poolFile.read())
poolFile.close()

answer = list()
used = {}
i = 0
def dfs(used, current, answer): # current = node address
    if str(trans[current][0])[:6] == "master":
        answer += trans[current]
    else:
        global i
        used[current] = 1
        print('in')
        for sender in trans[current]:
            if used.get(sender) == None:
                i += 1
                print(i)
                dfs(used, sender, answer)

dfs(used, userAddress, answer)

print(set(answer))

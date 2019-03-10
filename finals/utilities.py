import json

def getFile(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except:
        return -1

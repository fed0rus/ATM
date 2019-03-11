from subprocess import check_output
from time import sleep
import json
import re
from datetime import datetime

def setNet():
    try:
        with open("network.json", 'r') as file:
            config = json.load(file)
            return config
    except:
        return -1

def setUserId():
    try:
        with open("person.json", 'r') as file:
            id = json.load(file)
            return id
    except:
        return -1

def checkNumber(number):
    parsed = re.findall(r"\+\d+", number)
    if len(parsed) == 0:
        return False
    return parsed[0] == number and len(number) == 12

def getContract(flag):
    if flag == "kyc":
        compiledRegistrar = check_output(["solc", "--optimize", "--bin", "--abi", "-o", "./", "registrar.sol"]).decode()
        pass

def convertEpoch(unixTime):
    assert type(unixTime) == int
    return datetime.utcfromtimestamp(unixTime).strftime("%H:%M %d.%m.%Y")

print(setUserId())

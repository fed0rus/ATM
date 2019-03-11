from subprocess import check_output
from time import sleep
import json
import re

def getFile(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
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
        bytecode = 

getContract("kyc")

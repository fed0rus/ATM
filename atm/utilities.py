from subprocess import check_output
from time import sleep
import sys
import json
import re
from datetime import datetime

def net():
    try:
        with open("network.json", 'r') as file:
            config = json.load(file)
            return config
    except:
        return -1

def registrar():
    try:
        with open("registrar.json", 'r') as file:
            reg = json.load(file)
            return reg
    except:
        print("No contract address")
        sys.exit(1)

def userId():
    try:
        with open("person.json", 'r') as file:
            id = json.load(file)
            return id
    except:
        print("ID is not found")
        sys.exit(1)

def checkNumber(number):
    parsed = re.findall(r"\+\d+", number)
    if len(parsed) == 0:
        return False
    return parsed[0] == number and len(number) == 12

def binContract(flag):
    if flag == "kyc":
        data = dict()
        check_output(["solc", "--optimize", "--overwrite", "--bin", "--abi", "-o", "./", "Registrar.sol"])
        with open("Registrar.bin") as bin:
            data["bin"] = bin.read()
        with open("Registrar.abi") as abi:
            data["abi"] = abi.read()
        return data

    elif flag == "ph":
        data = dict()
        check_output(["solc", "--optimize", "--overwrite", "--bin", "--abi", "-o", "./", "Handler.sol"])
        with open("Handler.bin") as bin:
            with open("Handler.bin") as bin:
                data["bin"] = bin.read()
            with open("Handler.abi") as abi:
                data["abi"] = abi.read()
            return data
    else:
        raise ValueError

def convertEpoch(unixTime):
    assert type(unixTime) == int
    return datetime.utcfromtimestamp(unixTime).strftime("%H:%M %d.%m.%Y")

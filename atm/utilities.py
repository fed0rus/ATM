from subprocess import check_output
from time import sleep
import sys
import json
from datetime import datetime

def net():
    try:
        with open("network.json", 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print("Network configuration file is not found")

def userId():
    try:
        with open("person.json", 'r') as file:
            id = json.load(file)
            return "0x" + id["id"].replace('-', '')
    except FileNotFoundError:
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

def getContractAddress(flag):
    try:
        with open("registrar.json", 'r') as db:
            data = json.load(db)
        return (data["registrar"]["address"] if flag == "kyc" else data["payments"]["address"])
    except FileNotFoundError:
        print("No contract address")
        sys.exit(1)

def convertEpoch(unixTime):
    assert type(unixTime) == int
    return datetime.utcfromtimestamp(unixTime).strftime("%H:%M %d.%m.%Y")

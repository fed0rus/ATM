from subprocess import check_output
from time import sleep
import shutil
import sys
import os
import json
import argparse
from datetime import datetime

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--find', type=str, help="Find faces in the video")
    parser.add_argument('--actions', action='store_true', help="Select an action")
    parser.add_argument("--add", action="store", nargs='+', help="Send a request for registration")
    parser.add_argument("--balance", action="store", help="Get the balance of your account")
    parser.add_argument("--del", action="store", help="Delete a request for registration")
    parser.add_argument("--cancel", action="store", help="Cancel any request")
    parser.add_argument("--send", action="store", nargs='+', help="Send money by a phone number")
    parser.add_argument("--ops", action="store", help="List the payments history")
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("--owner", action="store", help="Acquire the owner of the contract")
    parser.add_argument("--chown", action="store", nargs='+', help="Transfer ownership of the contract")
    parser.add_argument("--test", action="store_true", help="Just for lulz")

    args = parser.parse_args()
    return vars(args)

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
    if len(parsed) == 0 or parsed[0] != number or len(number) != 12:
        print("Incorrect phone number")
        sys.exit(1)

def binContract(flag):
    if flag == "kyc":
        data = dict()
        check_output(["solc", "--optimize", "--overwrite", "--bin", "--abi", "-o", "./", "Registrar.sol"])
        with open("Registrar.bin", 'r') as bin:
            data["bin"] = bin.read()
        with open("Registrar.abi") as abi:
            data["abi"] = abi.read()
        os.remove("Registrar.bin")
        os.remove("Registrar.abi")
        return data

    elif flag == "ph":
        data = dict()
        check_output(["solc", "--optimize", "--overwrite", "--bin", "--abi", "-o", "./", "Handler.sol"])
        with open("Handler.bin") as bin:
            data["bin"] = bin.read()
        with open("Handler.abi") as abi:
            data["abi"] = abi.read()
        os.remove("Handler.bin")
        os.remove("Handler.abi")
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

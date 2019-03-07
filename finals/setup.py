#!/usr/bin/env python

from web3 import Web3, HTTPProvider

def setArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")

def main():
    with open("network.json", 'r') as ethConfig:
        rpcURL = str(json.load(ethConfig)["rpcUrl"])
        privateKey = str(json.load(ethConfig)["privKey"])
        gasPriceURL = str(json.load(ethConfig)["gasPriceUrl"])
        defaultGasPrice = str(json.load(ethConfig)["defaultGasPrice"])
    server = Web3(HTTPProvider(rpcURL))

if __name__ == "__main__":
    main()

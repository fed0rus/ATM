#!/usr/bin/env python

from web3 import Web3, HTTPProvider

web3 = Web3(HTTPProvider('https://sokol.poa.network'))

import argparse
from eth_account import Account
import requests

def main():
    args = set_args()
    args = vars(args)
    if (args['key'] != None and args['to'] == None):
        address = getAddress(args['key'])
        value = getBalance(address)
        value = scalingSum(value)
        unit = value[1]
        value = value[0]
        print('Balance on ' + '"' + address[2:] + '" is ' + str(round(value, 6)) + ' ' + unit)
    elif (args['key'] != None and args['to'] != None):
        from_address = getAddress(args['key'])
        to_address = '0x' + args['to']
        from_key = args['key']

        from_value = getBalance(from_address)
        if (from_value < args['value']):
            print('No enough funds for payment')
        else:
            value = int(args['value'])
            ident = identGenerate(from_address, to_address, value)
            signed_txn = web3.eth.account.signTransaction(ident, from_key)
            transaction_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            value = scalingSum(value)
            unit = value[1]
            value = value[0]
            print('Payment of ' + str(round(value, 6)) + ' ' + unit + ' to "' + to_address[2:] + '" scheduled')
            print('Transaction Hash: ' + str(transaction_hash.hex()))
    else:
        transaction_hash = args['tx']
        transaction_information = web3.eth.getTransaction(transaction_hash)
        if (transaction_information == None):
            print('No such transaction in the chain')
        elif (transaction_information['transactionIndex'] == 0):
            value = transaction_information['value']
            to_address = transaction_information['to'][2:]
            value = scalingSum(value)
            unit = value[1]
            value = value[0]
            print('Payment of ' + str(round(value, 6)) + ' ' + unit + ' to "' + str(to_address) + '" confirmed')
        else:
            value = transaction_information['value']
            to_address = transaction_information['to'][2:]
            value = scalingSum(value)
            unit = value[1]
            value = value[0]
            print('Delay in payment of ' + str(round(value, 6)) + ' ' + unit + ' to "' + str(to_address) + '"')

def identGenerate(from_address, to_address, value):
    res = dict()
    res['nonce'] = web3.eth.getTransactionCount(from_address)
    res['gasPrice'] = getGasPrice()
    res['gas'] = 21000
    res['to'] = to_address
    res['value'] = value
    return res

def getGasPrice():
    response = requests.get("https://gasprice.poa.network")
    res = response.json()['slow']
    return int((res - 0.2) * 1e9)

def scalingSum(value):
    p = ['wei', 'kwei', 'mwei', 'gwei', 'szabo', 'finney', 'poa']
    nowp = 0
    while (value >= 1000 and nowp < 6):
        value /= 1000
        nowp += 1
    return [value, p[nowp]]

def getAddress(user_key):
    address = str((Account.privateKeyToAccount(user_key)).address)
    return address

def getBalance(address):
    value = web3.eth.getBalance(address)
    return value


def set_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--key',
        help = 'sender key',
        type = str,
    )
    parser.add_argument(
        '--to',
        help = 'receiver key',
        type = str,
    )
    parser.add_argument(
        '--value',
        help = 'value of transaction',
        type = int,
    )
    parser.add_argument(
        '--tx',
        help = 'transaction hash',
        type = str,
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()

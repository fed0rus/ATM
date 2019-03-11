import requests

from time import sleep
from ethereum.utils import privtoaddr
from checkers import check_pin_code
from config import get
from subprocess import check_output
import re
from web3 import Web3

from output_util import print_error

RPC_URL = get('network.rpcUrl')

web3 = Web3(Web3.HTTPProvider(RPC_URL))

PRIVATE_KEY = bytes.fromhex(get('network.privKey'))

DEFAULT_GAS = 200000

try:
    GAS_PRICE = int(1000000000 * requests.get(get('network.gasPriceUrl')).json()['fast'])
except requests.exceptions.RequestException:
    GAS_PRICE = get('network.defaultGasPrice')

compiled_registrar = check_output(["solc", "--optimize", "--bin", "--abi", "./Registrar.sol"]).decode()
compiled_registrar_bytecode = re.findall("Binary: \\n(.*?)\\n", compiled_registrar)[0]

compiled_certificates = check_output(["solc", "--optimize", "--bin", "--abi", "Certificates.sol"]).decode()
compiled_certificates_bytecode = re.findall("Binary: \\n(.*?)\\n", compiled_certificates)[0]


def private_key_to_address(private_key):
    return web3.toChecksumAddress(privtoaddr(private_key).hex())


def build_and_send_tx(private_key, to='', data='', value=0, nonce=None):
    address = private_key_to_address(private_key)
    if nonce is None:
        nonce = web3.eth.getTransactionCount(address)
    tx = {
        'from': address,
        'to': to,
        'nonce': nonce,
        'data': data,
        'value': value,
        'gasPrice': GAS_PRICE,
        'gas': DEFAULT_GAS
    }

    signed = web3.eth.account.signTransaction(tx, private_key)

    tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

    return wait_tx_receipt(tx_hash)


def wait_tx_receipt(tx_hash, sleep_interval=0.5):
    while True:
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt:
            return tx_receipt
        sleep(sleep_interval)


def get_owner_nonce():
    return web3.eth.getTransactionCount(private_key_to_address(PRIVATE_KEY))


def deploy_contract(contract_name, nonce):
    bytecode = ''
    if contract_name == 'registrar':
        bytecode = compiled_registrar_bytecode
    elif contract_name == 'certificates':
        bytecode = compiled_certificates_bytecode

    tx_receipt = build_and_send_tx(PRIVATE_KEY, data=bytecode, nonce=nonce)

    return {"address": tx_receipt['contractAddress'], "startBlock": tx_receipt['blockNumber']}


def pin_code_to_private_key(pin_code):
    pin_code = check_pin_code(pin_code)
    person_id = get('person.id')
    if person_id is None:
        print_error('ID is not found')
    return get_private_key(person_id, pin_code)


def get_private_key(person_id, pin_code):
    id = bytes.fromhex(person_id.replace('-', ''))

    a = web3.keccak(bytes(0))
    b = web3.keccak(a + id + bytes([int(pin_code[0])]))
    c = web3.keccak(b + id + bytes([int(pin_code[1])]))
    d = web3.keccak(c + id + bytes([int(pin_code[2])]))
    return web3.keccak(d + id + bytes([int(pin_code[3])]))


def normalize_value(value):
    for currency in ['ether', 'finney', 'szabo', 'gwei', 'mwei', 'kwei', 'wei']:
        if web3.fromWei(value, currency) >= 1:
            return ('%.6f' % web3.fromWei(value, currency)).rstrip('0').rstrip('.') \
                   + ' %s' % (currency if currency != 'ether' else 'poa')
    return '0 poa'


def get_balance(address):
    return web3.eth.getBalance(address)

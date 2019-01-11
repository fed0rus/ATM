import web3
from web3 import Web3, HTTPProvider

server = Web3(HTTPProvider("https://sokol.poa.network/"))

contractAddress = server.toChecksumAddress('0xe87a3686b0a42d66eee76d48c9a8307c27d14d1c')
contractABI = [{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"withdraw","inputs":[{"type":"uint256","name":"_value"}],"constant":False},{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"transfer","inputs":[{"type":"bytes32","name":"_txHash"},{"type":"uint256","name":"_vout"},{"type":"address[]","name":"_recipients"},{"type":"uint256[]","name":"_values"}],"constant":False},{"type":"constructor","stateMutability":"nonpayable","payable":False,"inputs":[]},{"type":"fallback","stateMutability":"payable","payable":True},{"type":"event","name":"Transfer","inputs":[{"type":"bytes32","name":"tx_source","indexed":True},{"type":"bytes32","name":"tx_address","indexed":True},{"type":"address","name":"recipient","indexed":True},{"type":"uint256","name":"value","indexed":False},{"type":"uint256","name":"vout","indexed":False}],"anonymous":False}]

contract = server.eth.contract(address=contractAddress, abi=contractABI)

s = contract.events.Transfer({fromBlock: 0}, function(error, event){print(event);}).on('data', function)

import web3
from web3 import Web3, HTTPProvider
from eth_account import Account

server = Web3(HTTPProvider("https://sokol.poa.network/"))

contractAddress = server.toChecksumAddress("0xe87a3686b0a42d66eee76d48c9a8307c27d14d1c")

f = open("shit.txt", "w+")

filter = server.eth.filter({
  "fromBlock": 0,
  "toBlock": 'latest',
  "address": contractAddress
})
f.write(str(server.eth.getFilterLogs(filter.filter_id)))

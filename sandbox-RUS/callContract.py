import sys
sys.path.append("C:\Python_Interpreter\Lib\site-packages")

from web3 import Web3, HTTPProvider

def main():
    server = Web3(HTTPProvider("https://sokol.poa.network"))
    Final = server.eth.contract(address="0x107b1A1bfff3C07B4389876cbA750738c8cb42df", abi=[{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[{"type":"string","name":""}],"name":"retrieveData","inputs":[{"type":"address","name":"testAddress"}],"constant":False},{"type":"function","stateMutability":"nonpayable","payable":False,"outputs":[],"name":"deleteContract","inputs":[],"constant":False},{"type":"fallback","stateMutability":"payable","payable":True}]);
    response = Final.functions.retrieveData("0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69").call()
    print(response)

if __name__ == "__main__":
    main()

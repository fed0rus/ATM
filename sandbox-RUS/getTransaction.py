import sys
sys.path.append("C:\Python_Interpreter\Lib\site-packages")

from web3 import Web3, HTTPProvider

def main():
    server = Web3(HTTPProvider("https://sokol.poa.network"))
    print(server.eth.getTransaction("0x86900088d45dd00a36199a935e683fd582fadd9ca98fe03bea56109c569fb074"))

if __name__ == "__main__":
    main()
'''
{
    'blockHash': HexBytes('0x8b5d426961fd378c55b739689f289641bafcf0dfd86953fad062c0b19958086d'),
    'blockNumber': 7019045,
    'chainId': '0x4d',
    'condition': None,
    'creates': None,
    'from': '0xf4bF63D658BE2288697cCbE2c5697d9f19Af4e69',
    'gas': 43475,
    'gasPrice': 1000000000,
    'hash': HexBytes('0x86900088d45dd00a36199a935e683fd582fadd9ca98fe03bea56109c569fb074'),
    'input': '0x51e0556d',
    'nonce': 37,
    'publicKey': HexBytes('0x33ae3afebc646f247d1982a517d222727ca5158aecb77a41ae6fe41d7a339f0964561c9f7cf54d62ac401c4688c7abe69da9b46677716d1ec4a4e59675387cbb'),
    'r': HexBytes('0x334872631066a075329a4580af92c9b588003b4cadfa6a659432714c94521e6f'),
    'raw': HexBytes('0xf86825843b9aca0082a9d394b9d49c576186e5170ebbb07127c61432031fdaff808451e0556d81bda0334872631066a075329a4580af92c9b588003b4cadfa6a659432714c94521e6fa066e3ebd084fea0d13ce76bc1d30e403d04d059f6955ede32e4338fecbea6e213'),
    's': HexBytes('0x66e3ebd084fea0d13ce76bc1d30e403d04d059f6955ede32e4338fecbea6e213'),
    'standardV': 0,
    'to': '0xB9d49C576186E5170eBBb07127C61432031FdAFf',
    'transactionIndex': 0,
    'v': 189,
    'value': 0
}
'''

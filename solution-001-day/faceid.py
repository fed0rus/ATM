from argparse import ArgumentParser

from blockchain import get_balance, private_key_to_address, pin_code_to_private_key, normalize_value

parser = ArgumentParser(prog='Faceid service')

parser.add_argument('--balance',
                    nargs=1,
                    metavar='PIN_CODE',
                    type=pin_code_to_private_key,
                    help='Prints user balance')
args = parser.parse_args()

if args.balance:
    private_key = args.balance[0]
    address = private_key_to_address(private_key)

    print('Your balance is %s' % normalize_value(get_balance(address)))

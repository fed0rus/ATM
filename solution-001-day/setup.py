from argparse import ArgumentParser

from blockchain import deploy_contract, get_owner_nonce
from config import set

parser = ArgumentParser(prog='Setup')

parser.add_argument('--deploy',
                    action='store_true',
                    help='Deploys registrar and certificates contracts to the blockchain')


args = parser.parse_args()

if args.deploy:
    nonce = get_owner_nonce()
    registrar = deploy_contract('registrar', nonce)
    print('KYC Registrar: %s' % registrar['address'])
    set('registrar.registrar', registrar)

    certificates = deploy_contract('certificates', nonce + 1)
    print('Payment Handler: %s' % certificates['address'])
    set('registrar.payments', certificates)

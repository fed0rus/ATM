import argparse

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
    parser.add_argument("--chown", action="store", nargs='+', help="Change the owner of the contract")

    args = parser.parse_args()
    return vars(args)

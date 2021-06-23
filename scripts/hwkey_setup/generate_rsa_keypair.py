import pkcs11
import argparse
from ALIIAS.utility import find_opensc_lib


parser = argparse.ArgumentParser(description='Init HW key with the specified PIN')
parser.add_argument('-p', '--pin', type=str, help='pin code for the key')

args = parser.parse_args()

if __name__ == '__main__':
    lib = find_opensc_lib()

    # token = lib.get_token(token_label="Nitrokey (UserPIN)")
    token = lib.get_token()

    # In case of the "pkcs11.exceptions.MultipleObjectsReturned: More than 1 key matches"
    # re-initialize the token with sc-hsm-tool

    with token.open(user_pin=args.pin, rw=True) as session:
        # Generate an RSA keypair in this session
        # this only has to be done once, and shouldn't be part of PseudoID (only as a utility to set up keys)
        # comment this out if key was already generated, or re-initialize (see above)
        pub, priv = session.generate_keypair(pkcs11.KeyType.RSA, 2048)

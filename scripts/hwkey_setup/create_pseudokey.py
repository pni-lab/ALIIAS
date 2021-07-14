import argparse
from Crypto.Random import get_random_bytes
import binascii
from os import path

parser = argparse.ArgumentParser(description='Generate a new 32 byte pseudokey and write it to a txt file')
parser.add_argument('-k', '--projectkey', type=str, help='key for the project')

args = parser.parse_args()

if __name__ == '__main__':
    filename = args.projectkey + '_pseudokey.txt'
    key = binascii.hexlify(get_random_bytes(32)).decode('utf-8')
    if not path.exists(filename):
        with open(filename, "w") as file:
            file.write(key)
        print('Project: ' + args.projectkey)
        print('Pseudokey: ' + key)
    else:
        print('file already exists!')

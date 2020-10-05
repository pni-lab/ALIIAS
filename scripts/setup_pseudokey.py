import argparse
from Crypto.Random import get_random_bytes
import binascii
from os import path

parser = argparse.ArgumentParser(description='generate pseudokey, write to txt')
parser.add_argument('-p', '--project', type=str, help='name of the project')

args = parser.parse_args()

if __name__ == '__main__':
    filename = args.project + '_pseudokey.txt'
    key = binascii.hexlify(get_random_bytes(32)).decode('utf-8')
    if not path.exists(filename):
        with open(filename, "w") as file:
            file.write(key)
        print(args.project)
        print(key)
    else:
        print('file already exists!')

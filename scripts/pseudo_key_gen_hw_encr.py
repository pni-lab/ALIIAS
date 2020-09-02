import binascii
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import pkcs11
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.util.rsa import encode_rsa_public_key

# generate random pseudonymisation key (pkey)
# encrypt the pkey with the hw_key
# ToDo: store encrypted key in config file


pseudo_key = get_random_bytes(32)
print('pseudo key', pseudo_key)

lib = pkcs11.lib('/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so')
token = lib.get_token()

with token.open(user_pin='648219', rw=True) as session:
    # Extract public key
    hw_key = session.get_key(key_type=KeyType.RSA,
                             object_class=ObjectClass.PUBLIC_KEY)
    hw_key = RSA.importKey(encode_rsa_public_key(hw_key))

    # Encryption on the local machine
    cipher = PKCS1_v1_5.new(hw_key)
    crypttext = cipher.encrypt(pseudo_key)

    print('pkey encrypted: ', crypttext)

    # Decryption in the HSM
    priv = session.get_key(key_type=KeyType.RSA,
                           object_class=ObjectClass.PRIVATE_KEY)

    plaintext = priv.decrypt(crypttext, mechanism=Mechanism.RSA_PKCS)

    print('pseudo key decrypted: ', plaintext)

print('encryption successful: ', pseudo_key == plaintext)

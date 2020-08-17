import pkcs11
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.util.rsa import encode_rsa_public_key

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import os

#lib = pkcs11.lib(os.environ['PKCS11_MODULE'])
lib = pkcs11.lib('/usr//local/lib/opensc-pkcs11.so')


#token = lib.get_token(token_label="Nitrokey (UserPIN)")
token = lib.get_token()

data = b'INPUT DATA'

# Open a session on our token
#sc-hsm-tool --initialize --so-pin 3537363231383830 --pin 648219 --label "Nitrokey"
with token.open(user_pin='648219', rw=True) as session:
    # Generate an RSA keypair in this session
    #pub, priv = session.generate_keypair(pkcs11.KeyType.RSA, 2048)

    # Extract public key
    key = session.get_key(key_type=KeyType.RSA,
                          object_class=ObjectClass.PUBLIC_KEY)
    key = RSA.importKey(encode_rsa_public_key(key))

    # Encryption on the local machine
    cipher = PKCS1_v1_5.new(key)
    crypttext = cipher.encrypt(b'Data to encrypt')

    # Decryption in the HSM
    priv = session.get_key(key_type=KeyType.RSA,
                                object_class=ObjectClass.PRIVATE_KEY)

    plaintext = priv.decrypt(crypttext, mechanism=Mechanism.RSA_PKCS)

    print(plaintext)
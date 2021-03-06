import pkcs11
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.util.rsa import encode_rsa_public_key

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import os

#lib = pkcs11.lib(os.environ['PKCS11_MODULE'])
#lib = pkcs11.lib('/usr//local/lib/opensc-pkcs11.so')
lib = pkcs11.lib('/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so')
#lib = pkcs11.lib('C:/Program Files/OpenSC Project/OpenSC/pkcs11/opensc-pkcs11.dll')



#token = lib.get_token(token_label="Nitrokey (UserPIN)")
token = lib.get_token()
 
# Open a session on our token
# token was initialized with:
#sc-hsm-tool --initialize --so-pin 3537363231383830 --pin 289289 --label "Nitrokey"
# In case of the "pkcs11.exceptions.MultipleObjectsReturned: More than 1 key matches"
# re-initialize the token with sc-hsm-tool
#
with token.open(user_pin='289289', rw=True) as session:
    # Generate an RSA keypair in this session
    # this only has to be done once, and shouldn't be part of PseudoID (only as a utility to set up keys)
    # comment this out if key was already generated, or re-initialize (see above)
    # pub, priv = session.generate_keypair(pkcs11.KeyType.RSA, 2048)

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
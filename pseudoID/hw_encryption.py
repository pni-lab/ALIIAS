import binascii
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import pkcs11
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.util.rsa import encode_rsa_public_key
import configparser
import warnings

config = configparser.ConfigParser()
config.read('../pseudoID/settings.conf')

# ToDo: store encrypted key in config file

class HardwareEncryptor:
    """
    # example
    nitrokey = HardwareEncryptor()
    nitrokey.gen_new_pseudokey()
    print(nitrokey.pseudokey)
    pseudokey_encrypted = nitrokey.encrypt()
    nitrokey.decrypt(pseudokey_encrypted)

    """
    def __init__(self):
        path_opensc = config['BASE']['opensc_path']
        self.lib = pkcs11.lib(path_opensc)

        try:
            self.token = self.lib.get_token()
        except pkcs11.exceptions.NoSuchToken:
            warnings.warn('Dongle not plugged in!')

        return

    def gen_new_pseudokey(self):
        self.pseudokey = get_random_bytes(32)
        return

    def read_encrypted_pseudokey(self):
        # todo:
        # self.pseudokey_encrypted
        return

    def encrypt(self, pseudokey=None):
        if not pseudokey: pseudokey = self.pseudokey

        with self.token.open(user_pin='648219', rw=True) as session:
            # Extract public key
            hw_key = session.get_key(key_type=KeyType.RSA,
                                     object_class=ObjectClass.PUBLIC_KEY)
            hw_key = RSA.importKey(encode_rsa_public_key(hw_key))

            # Encryption on the local machine
            cipher = PKCS1_v1_5.new(hw_key)
            crypttext = cipher.encrypt(pseudokey)
        return crypttext

    def decrypt(self, pseudokey_encrypted):
        if not pseudokey_encrypted: pseudokey = self.pseudokey_encrypted

        with self.token.open(user_pin='648219', rw=True) as session:
            # Extract public key
            hw_key = session.get_key(key_type=KeyType.RSA,
                                     object_class=ObjectClass.PUBLIC_KEY)
            hw_key = RSA.importKey(encode_rsa_public_key(hw_key))

            # Decryption in the HSM
            priv = session.get_key(key_type=KeyType.RSA,
                                   object_class=ObjectClass.PRIVATE_KEY)

            plaintext = priv.decrypt(pseudokey_encrypted, mechanism=Mechanism.RSA_PKCS)
        return plaintext



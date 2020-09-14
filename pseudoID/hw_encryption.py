import binascii
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
import pkcs11
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.util.rsa import encode_rsa_public_key
import warnings
from pseudoID import config
from pseudoID.base_conversion import BaseConverter


# ToDo: store encrypted key in config file
conv = BaseConverter(config.settings['ENCRYPTION']['char_base'])


class HardwareEncryptor:
    """
    # example
    nitrokey = HardwareEncryptor()
    nitrokey.gen_new_pseudokey()
    print(nitrokey.pseudokey)
    pseudokey_encrypted = nitrokey.encrypt()
    nitrokey.decrypt(pseudokey_encrypted)

    """

    def __init__(self, test=True): #todo remove this
        path_opensc = config.settings['BASE']['opensc_path']
        self.lib = pkcs11.lib(path_opensc)
        if not test:
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


class SessionHandler:
    def __init__(self):
        super().__init__()
        self.user_key = config._user_key_

    def encrypt(self, plaintext):
        cipher = AES.new(self.user_key, AES.MODE_SIV)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.rjust(64, '0').encode("utf-8"))

        return conv.hex2custom(binascii.hexlify(ciphertext + tag).decode('utf-8'))

    def decrypt(self, decrypt_me):
        decrypt_me=conv.custom2hex(decrypt_me)
        tag = binascii.unhexlify(decrypt_me[-32:].encode('utf-8'))
        message = binascii.unhexlify(decrypt_me[:-32].encode('utf-8'))
        cipher = AES.new(self.user_key, AES.MODE_SIV)
        plaintext = cipher.decrypt_and_verify(message, mac_tag=tag)

        return plaintext.decode('utf-8').lstrip('0')

    def set(self, path=config.HANDLER_DIR):
        with open(path, "r") as file:
            handles = file.readlines()
            for line in handles:
                helper = self.decrypt(line[:-1]).split(" ")
                if len(helper) == 4 and helper[1] == "SFB289":
                    self.site=helper[2]
                    self.site_tag=helper[3]
                    self.pseudo_key=helper[0].encode("utf-8")

    def extend(self, entry, path=config.HANDLER_DIR):
        with open(path, "a") as file:
            file.writelines(self.encrypt(entry) + "\n")




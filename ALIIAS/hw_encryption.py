import binascii
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, AES
import pkcs11
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.util.rsa import encode_rsa_public_key
import warnings
import os.path as path
from ALIIAS import config
from ALIIAS.base_conversion import BaseConverter
import hashlib
from ALIIAS.utility import find_opensc_lib
from abc import ABC, abstractmethod

# ToDo: store encrypted key in config file
conv = BaseConverter(config.settings['ENCRYPTION']['char_base'])


class EncryptorBase(ABC):
    @abstractmethod
    def encrypt(self):
        pass

    @abstractmethod
    def decrypt(self):
        pass


class HardwareEncryptor(EncryptorBase):
    """
    # example
    config.DONGLE_PIN = # needs to be set
    nitrokey = HardwareEncryptor()
    text = b"Hello World!"
    ciphertext = nitrokey.encrypt(text)
    plaintext = nitrokey.decrypt(binascii.hexlify(ciphertext))

    """

    def __init__(self):  # todo: init this class with the pin, so it can be used in the setup process
        self.no_dongle = False
        # a wild exception handler chain for finding opensc
        self.lib = find_opensc_lib()

        try:
            self.token = self.lib.get_token()
            self.label = self.token.label.split(" ")[0]
            print("Token Label: " + self.label)
            # todo: catch when no pin is entered and check number of wrong pin entries
            if config.DONGLE_PIN is not None:
                self.session = self.token.open(user_pin=config.DONGLE_PIN, rw=True)
        except pkcs11.exceptions.NoSuchToken:
            warnings.warn('Dongle not plugged in!')
            self.no_dongle = True
        return

    def gen_new_pseudokey(self):
        self.pseudokey = get_random_bytes(32)
        return

    def read_encrypted_pseudokey(self):
        # todo:
        # self.pseudokey_encrypted
        return

    def encrypt(self, plaintext=None):
        # if not plaintext: plaintext = self.pseudokey

        # ToDo: ask for pin for REAL 2FA
        # Extract public key
        hw_key = self.session.get_key(key_type=KeyType.RSA,
                                      object_class=ObjectClass.PUBLIC_KEY)
        hw_key = RSA.importKey(encode_rsa_public_key(hw_key))

        # Encryption on the local machine
        cipher = PKCS1_v1_5.new(hw_key)
        crypttext = cipher.encrypt(plaintext)
        return crypttext

    def decrypt(self, ciphertext):
        priv = self.session.get_key(key_type=KeyType.RSA,
                                    object_class=ObjectClass.PRIVATE_KEY)

        plaintext = priv.decrypt(binascii.unhexlify(ciphertext), mechanism=Mechanism.RSA_PKCS)
        return plaintext.decode('utf-8')

    def close(self):
        self.session.close()


class OfflineEncryptor(EncryptorBase):
    def __init__(self):
        self.offline_key = config._offline_key_

    def encrypt(self, plaintext):
        cipher = AES.new(self.offline_key, AES.MODE_SIV)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))

        return binascii.hexlify(ciphertext + tag).decode('utf-8')

    def decrypt(self, ciphertext):
        ciphertext = binascii.hexlify(ciphertext)
        tag = ciphertext[-32:]
        message = ciphertext[:-32]
        cipher = AES.new(self.offline_key, AES.MODE_SIV)
        plaintext = cipher.decrypt_and_verify(message, mac_tag=tag)
        return binascii.hexlify(plaintext)


class DemoHandler:
    def __init__(self):
        self.no_dongle = False
        return

    def set(self):
        self.site = config.settings['DEMO']['key_tag']
        self.site_tag = config.settings['DEMO']['site_tag']
        self.pseudo_key = config.settings['DEMO']['pseudo_key'].encode("utf-8")



# class SessionHandler(HardwareEncryptor if not config.settings['ENCRYPTION']['offline'] else OfflineEncryptor):
class SessionHandler(HardwareEncryptor):
    def __init__(self):
        super().__init__()

    def set(self, path=config.HANDLER_DIR):
        if self.no_dongle:
            self.site = self.site_tag = self.pseudo_key = self.label = None

            return
        with open(path, "rb") as file:
            handles = file.read().splitlines()
            for line in handles:
                handle = line.decode('utf-8').split('_')

                if self.label == handle[0]:
                    try:
                        helper = self.decrypt(handle[1]).split('_')
                        hash_obj = hashlib.md5(helper[1].encode('utf-8'))
                        valid_tag_hash = hash_obj.hexdigest()
                        # todo: need to be fixed for the sfb version
                        if (valid_tag_hash == config.settings['ENCRYPTION']['validation_tag']) or \
                                helper[1] == config.settings['ENCRYPTION']['validation_tag_default']:
                            # if helper[1] == config.settings['ENCRYPTION']['validation_tag_default']:
                            # print(helper[2])
                            self.site = helper[2]
                            print("Site: " + self.site)
                            self.site_tag = helper[3]
                            self.pseudo_key = helper[0].encode("utf-8")
                            # break

                    except:
                        print('oops, wrong key!')

        self.close()

    def extend(self, entry, path=config.HANDLER_DIR):
        with open(path, "ab") as file:
            file.write(entry)
            file.write(b'\n')

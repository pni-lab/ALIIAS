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
import hashlib

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

    def __init__(self):  # todo remove this
        path_opensc = config.settings['BASE']['opensc_path']
        self.lib = pkcs11.lib(path_opensc)
        try:
            self.token = self.lib.get_token()
            self.label = self.token.label[0:3]
            print("Token Label: " + self.label)
            self.session = self.token.open(user_pin='289289', rw=True)
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

    def encrypt(self, plaintext=None):
        if not plaintext: plaintext = self.pseudokey

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


class OfflineEncryptor:
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


# class SessionHandler(HardwareEncryptor if not config.settings['ENCRYPTION']['offline'] else OfflineEncryptor):
class SessionHandler(HardwareEncryptor):
    def __init__(self):
        super().__init__()

    def set(self, path=config.HANDLER_DIR):
        with open(path, "rb") as file:
            handles = file.read().splitlines()
            for line in handles:
                if self.label == line[0:3].decode('utf-8'):
                    try:
                        helper = self.decrypt(line[3:]).split('_')

                        hash_obj = hashlib.md5(helper[1].encode('utf-8'))
                        valid_tag_hash = hash_obj.hexdigest()

                        if valid_tag_hash == config.settings['ENCRYPTION']['validation_tag']:
                            # print(helper[2])
                            self.site = helper[2]
                            print("Site: " + self.site)
                            self.site_tag = helper[3]
                            self.pseudo_key = helper[0].encode("utf-8")
                            break
                    except:
                        print('something went wrong when trying to access the key!')

        self.close()

    def extend(self, entry, path=config.HANDLER_DIR):
        with open(path, "ab") as file:
            file.write(entry)
            file.write(b'\n')

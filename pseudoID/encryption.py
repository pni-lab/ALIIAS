import binascii
import hashlib
import config

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Encryptor:
    def __init__(self, user_key=config._user_key_, pseudonym_key_encripted=config._pseudonym_key_encripted_):

        cipher = AES.new(user_key, AES.MODE_SIV)
        self.key = cipher.decrypt_and_verify(pseudonym_key_encripted[0],
                                             pseudonym_key_encripted[1])

    def long_id(self, message):
        cipher = AES.new(self.key, AES.MODE_SIV)
        ciphertext, tag = cipher.encrypt_and_digest(message.rjust(64, '0').encode("utf-8"))

        return binascii.hexlify(ciphertext)
        #return hashlib.sha3_256(binascii.hexlify(ciphertext)).hexdigest()[0:8]

    def short_id(self, long_id, length=8): #ToDo: length from conf file
        return long_id[0:length]

    def reidentify(self, longID):
        #unhexlify
        pass
        #cipher = AES.new(self.key, AES.MODE_SIV)
        #data = self.cipher.decrypt(message.rjust(64, '0').encode("utf-8"))


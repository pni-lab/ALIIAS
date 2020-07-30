import binascii
import hashlib
import config
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Encryptor:
    def __init__(self, user_key=config._user_key_, pseudonym_key_encripted=config._pseudonym_key_encripted_):
        self.iv = b'0123456789abcdef'
        self.key = b'e7d97fa7c1cc8a4e2489basd1f09a9d3'

    def long_id(self, message):
        cipher = AES.new(self.key, AES.MODE_OFB, iv=self.iv)
        ciphertext = cipher.encrypt(message.ljust(64, '0').encode("utf-8"))
        # return longid as string
        return b64encode(ciphertext).decode('utf-8')
        # return hashlib.sha3_256(binascii.hexlify(ciphertext)).hexdigest()[0:8]

    def short_id(self, long_id, length=8):  # ToDo: length from conf file
        return long_id[0:length]

    def reidentify(self, longID):
        cipher = AES.new(self.key, AES.MODE_OFB, iv=self.iv)
        pt = cipher.decrypt(b64decode(longID))
        return pt.decode("utf-8").rstrip('0')
        # unhexlify
        # pass
        # cipher = AES.new(self.key, AES.MODE_SIV)
        # data = self.cipher.decrypt(message.rjust(64, '0').encode("utf-8"))

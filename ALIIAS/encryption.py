import binascii

from Crypto.Cipher import AES
from ALIIAS import config
from ALIIAS.base_conversion import BaseConverter

conv = BaseConverter(config.settings['ENCRYPTION']['char_base'])

class Encryptor:
    # todo check old references for encryptor
    def __init__(self, pseudonym_key, site_tag=None):
        self.site_tag = site_tag
        self.key = pseudonym_key

        # dummy encryption to determine block length
        if self.site_tag is not None:
            self.encrypted_message_length = len(self._encrypt("a a a 01011999 a"))

    def _encrypt(self, message):
        cipher = AES.new(self.key, AES.MODE_SIV)
        ciphertext, tag = cipher.encrypt_and_digest(message.rjust(64, '0').encode("utf-8"))
        return binascii.hexlify(ciphertext + tag).decode('utf-8')

    def get_long_id(self, message):

        long_id = conv.hex2custom(self._encrypt(message))

        if self.site_tag is not None:
            long_id = self.site_tag + long_id
        return long_id

    def get_short_id(self, long_id, length=config.settings['ENCRYPTION'].getint('short_id_length')):
        if self.site_tag is None:
            return long_id[0:length]
        else:
            return long_id[0:length + 1]

    def reidentify(self, longID):
        if self.site_tag != None:
            longID = str(longID[1:])

        longID = conv.custom2hex(longID)
        # pad with zeros
        longID = longID.rjust(self.encrypted_message_length, '0')


        tag = binascii.unhexlify(longID[128:].encode('utf-8'))
        message = binascii.unhexlify(longID[:128].encode('utf-8'))

        cipher = AES.new(self.key, AES.MODE_SIV)
        plaintext = cipher.decrypt_and_verify(message, mac_tag=tag)

        return plaintext.decode('utf-8').lstrip('0')
        # data = self.cipher.decrypt(message.rjust(64, '0').encode("utf-8"))

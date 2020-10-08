from pseudoID.hw_encryption import OfflineEncryptor, SessionHandler
from pseudoID import config
import binascii

pseudo_key = b't\xfa\xad\xad\xe7\xb8\xaa\xc5\xb2;W\x84\xe1O2TZ\xdd\xf8\xbe\x80\xa4TG\xc8OS\xee\xf2\x9f\xa7v'
valid_tag = 'SFB289'
site = "Test"
site_tag = config._site_tag_[site]

suffix = '_' + valid_tag + '_' + site + '_' + site_tag

new_entry = binascii.hexlify(pseudo_key).decode('utf-8') + suffix

handler = SessionHandler()

cipher = handler.encrypt(new_entry)


# handler.extend(cipher.encode('utf-8'))

handler.set()

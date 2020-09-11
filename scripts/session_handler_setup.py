import binascii

from pseudoID.hw_encryption import SessionHandler

pseudo_key = b't\xfa\xad\xad\xe7\xb8\xaa\xc5\xb2;W\x84\xe1O2TZ\xdd\xf8\xbe\x80\xa4TG\xc8OS\xee\xf2\x9f\xa7v'
valid_tag = 'SFB289'
site = "A01"
site_tag = "a"

handler = SessionHandler()
new_entry = binascii.hexlify(pseudo_key).decode('utf-8') + ' ' + valid_tag + ' ' + site + ' ' + site_tag
handler.extend(new_entry)




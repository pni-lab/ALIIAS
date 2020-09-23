import binascii
from pseudoID import config
from pseudoID.hw_encryption import SessionHandler

pseudo_key = b't\xfa\xad\xad\xe7\xb8\xaa\xc5\xb2;W\x84\xe1O2TZ\xdd\xf8\xbe\x80\xa4TG\xc8OS\xee\xf2\x9f\xa7v'
valid_tag = 'SFB289'
site = "A01"
site_tag = config._site_tag_[site]

handler = SessionHandler()
new_entry = binascii.hexlify(pseudo_key).decode('utf-8') + '_' + valid_tag + '_' + site + '_' + site_tag


print(len(new_entry))
cipher = handler.encrypt(new_entry)
print(cipher)
print(len(cipher))
plaintext = handler.decrypt(cipher)
print(plaintext)
print(len(plaintext))
print(len(pseudo_key))

#handler.extend(new_entry)

#handler.set()
#print(handler.site_tag)
#handler.extend(new_entry, path='/home/renglert/PycharmProjects/PseudoID_v2/delete_me/handler.txt')



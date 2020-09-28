from pseudoID.hw_encryption import SessionHandler
import binascii
from pseudoID import config
from pseudoID.hw_encryption import SessionHandler

# ------------------- #
# CHANGE ME
site = "A01"
add_new_entry = False
# ------------------- #

valid_tag = 'SFB289'
site_tag = config._site_tag_[site]

nitro = SessionHandler()
nitro.gen_new_pseudokey()

suffix = '_' + valid_tag + '_' + site + '_' + site_tag

plaintext = binascii.hexlify(nitro.pseudokey).decode('utf-8') + suffix
new_entry = nitro.encrypt(plaintext.encode('utf-8'))

print(new_entry)

decr = nitro.decrypt(new_entry)

if add_new_entry:
    nitro.extend(new_entry)

#nitro.set()


import pickle
from Crypto.Cipher import AES

_user_key_file_ = '/key/user_key.pckl'
with open(_user_key_file_, 'br') as f:
    _user_key_ = pickle.load(f)

_pseudonym_key_encripted_ = (b'\xf2\xe6\xaf\xc6\x81\x06\xb3~\xd19\x1f\x0b\x01zE\x8ccn\xea\xcb\xd1N\x11H\xf3\xc5\x99\x10#\x0f\xe2\xdc',
                             b'\xbd2n\xb9\x91\xff\x82\xec\xb8\xa3\xd7\xefw@\xb73')

_ls_rc_url_ = 'https://www.uni-due.de/~ht2203/limesurvey/index.php/admin/remotecontrol'
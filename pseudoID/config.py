import pickle
from Crypto.Cipher import AES
from flask import Flask, redirect, url_for

app = Flask(__name__)

_key_dir_ = "../dev_key"   # root directory of the USB-stick. to be mounted to the docker container

_user_key_file_ = _key_dir_ + '/.user_key.pckl'

try:
    with open(_user_key_file_, 'br') as f:
        _user_key_ = pickle.load(f)
except:
    raise Exception('Something went wrong while loading the Encryption Key. '
                    'Please check if your USB drive is plugged in correctly and retry!')

_pseudonym_key_encrypted_ = (
    b'\xf2\xe6\xaf\xc6\x81\x06\xb3~\xd19\x1f\x0b\x01zE\x8ccn\xea\xcb\xd1N\x11H\xf3\xc5\x99\x10#\x0f\xe2\xdc',
    b'\xbd2n\xb9\x91\xff\x82\xec\xb8\xa3\xd7\xefw@\xb73')

_ls_url_base_ = 'https://www.uni-due.de/~ht2203/limesurvey'
_ls_url_rc_ = _ls_url_base_ + '/index.php/admin/remotecontrol'
_ls_url_login_ = _ls_url_base_ + "/index.php/admin/authentication/sa/login"

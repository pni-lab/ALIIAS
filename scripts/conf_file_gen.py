import configparser
from pseudoID import config
import os
import hashlib

# sc: https://linuxhint.com/read_write_ini_conf_python/

cfg_parser = configparser.ConfigParser()

# hash_obj = hashlib.md5(valid_tag)
valid_tag_hash = '281d5a4c850bdfbd9ec1bf34d9629ed8'

opensc_robert = 'C:/Program Files/OpenSC Project/OpenSC/pkcs11/opensc-pkcs11.dll'
opensc_tamas = '/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so'
opensc_ghouse = '/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so'

cfg_parser['BASE'] = {"Log_level": 10,
                      "opensc_path": opensc_robert,
                      "url": 'http://127.0.0.1:5000/',
                      "handler_name": "handler"}

cfg_parser['PSEUDOKEYS'] = {}

cfg_parser['ENCRYPTION'] = {"Type": "AES",
                            "short_id_length": "8",
                            "char_base": "123456789abcdefghjkmnpqrstuvwxyz",
                            "offline": False,
                            "validation_tag": valid_tag_hash}

_ls_url_base_ = 'https://sfb289.survey.uni-due.de'

cfg_parser['LIMESURVEY'] = {"active": True,
                            "url_base": _ls_url_base_,
                            "url_rc": _ls_url_base_ + '/index.php/admin/remotecontrol',
                            "url_login": _ls_url_base_ + '/index.php/admin/authentication/sa/login'}

cfg_parser['SITE_TAGS'] = {"Test": "t",
                           "A01": "1",
                           "A02": "2",
                           "A03": "3",
                           "A04": "4",
                           "A06": "6",
                           "A07": "7",
                           "A08": "8",
                           "A09": "9",
                           "A11": "a",
                           "A12": "b",
                           "A13": "c",
                           "A15": "e",
                           "A16": "f",
                           "B12": "g"}

cfg_parser['BARCODES'] = {"x_dim": 750, "y_dim": 375, "label_gap": 20, "n_diff_bc": 6, "n_identical_bc": 3,
                          "blank": True}

with open(os.path.join(config.ROOT_DIR, '../pseudoID/settings.conf'), 'w') as configfile:
    cfg_parser.write(configfile)

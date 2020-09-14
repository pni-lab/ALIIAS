import configparser
from pseudoID import config
import os
# sc: https://linuxhint.com/read_write_ini_conf_python/

cfg_parser = configparser.ConfigParser()

cfg_parser['BASE'] = {"Log_level": 10,
                  "opensc_path": '/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so'}

cfg_parser['PSEUDOKEYS'] = {}

cfg_parser['ENCRYPTION'] = {"Type": "AES",
                        "short_id_length": "8",
                        "char_base": "123456789abcdefghjkmnpqrstuvwxyz"}

_ls_url_base_ = 'https://www.uni-due.de/~ht2203/limesurvey_sfb289_test'

cfg_parser['LIMESURVEY'] = {"active": True,
                        "url_base": _ls_url_base_,
                        "url_rc": _ls_url_base_ + '/index.php/admin/remotecontrol',
                        "url_login": _ls_url_base_ + '/index.php/admin/authentication/sa/login'}

cfg_parser['BARCODES'] = {"x_dim": 750, "y_dim": 375, "label_gap": 20, "n_diff_bc": 6, "n_identical_bc": 3, "blank": True}

with open(os.path.join(config.ROOT_DIR, '../pseudoID/settings.conf'), 'w') as configfile:
    cfg_parser.write(configfile)

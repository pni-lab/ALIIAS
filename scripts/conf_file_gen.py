import configparser
from ALIIAS import config
import os
import hashlib
from ALIIAS._version import get_versions


# sc: https://linuxhint.com/read_write_ini_conf_python/

cfg_parser = configparser.ConfigParser()

# hash_obj = hashlib.md5(valid_tag)
valid_tag_hash = ''

__version__ = get_versions()['version']
del get_versions

cfg_parser['BASE'] = {"Log_level": 10,
                      "url": 'http://127.0.0.1:5000/',
                      "handler_name": "handler",
                      "version": str(__version__)}

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
                           "B12": "g",
                           "A05": "h"}

cfg_parser['BARCODES'] = {"x_dim": 750, "y_dim": 375, "label_gap": 20, "n_diff_bc": 6, "n_identical_bc": 3,
                          "blank": True}

with open(os.path.join(config.ROOT_DIR, '../ALIIAS/settings.conf'), 'w') as configfile:
    cfg_parser.write(configfile)

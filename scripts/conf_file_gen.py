import configparser

# sc: https://linuxhint.com/read_write_ini_conf_python/

config = configparser.ConfigParser()

_exp_tag_ = {
    "": "",
    "Pre": "-pre",
    "Post": "-post",
    "Baseline": "-bsl",
    "Week 1": "-wk1",
    "Week 2": "-wk2",
    "Week 3": "-wk3",
    "Week 4": "-wk4",
}

config['BASE'] = {"Log_level": 10,
                  "exp_tag": _exp_tag_,
                  "opensc_path": '/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so'}

config['PSEUDOKEYS'] = {}

config['ENCRYPTION'] = {"Type": "AES", "short_id_length": "8"}

_ls_url_base_ = 'https://www.uni-due.de/~ht2203/limesurvey'

config['LIMESURVEY'] = {"active": True,
                        "url_base": _ls_url_base_,
                        "url_rc": _ls_url_base_ + '/index.php/admin/remotecontrol',
                        "url_login": _ls_url_base_ + '/index.php/admin/authentication/sa/login'}

config['BARCODES'] = {"n_diff_bc": 6, "n_identical_bc": 3}

with open('../pseudoID/settings.conf', 'w') as configfile:
    config.write(configfile)

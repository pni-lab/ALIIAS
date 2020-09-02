import configparser
# sc: https://linuxhint.com/read_write_ini_conf_python/

config = configparser.ConfigParser()

config['DEFAULT'] = {"Log Level": 10}

config['PSEUDOKEYS'] = {}

config['ENCRYPTION'] = {"Type": "AES", "short_id_length": "8"}

config['LIMESURVEY'] = {}

config['BARCODES'] = {"n_diff_bc": 6, "n_identical_bc": 3}


with open('../pseudoID/settings.conf', 'w') as configfile:
    config.write(configfile)


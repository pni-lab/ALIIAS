from ALIIAS.barcode_gen import generate_barcode_set
from ALIIAS import config


short_id = "wwwwwwww"
site_tag = config.settings['SITE_TAGS']['A01']

if len(short_id) == int(config.settings['ENCRYPTION']['short_id_length']):
    barcodes = generate_barcode_set(site_tag + short_id)
else:
    print("string too short")




import barcode
from barcode.writer import ImageWriter
import PIL
from PIL import Image, ImageFont
import pseudoID.config as config
import pathlib
import os


def generate_barcode(short_ID, outdir=config.BC_DIR):

    writer = ImageWriter()
    bc = barcode.get('code128', short_ID, writer=writer)
    filename = bc.save(pathlib.Path(outdir).joinpath('barcode_' + short_ID),
                       {"module_width": 38.1 / 110,
                        "module_height": 19.05,
                        "text_distance": 1.0,
                        "font_size": 40})

    to_be_resized = Image.open(filename)

    newSize = (750, 375)  # for 38.1mmx19.05mm at 500dpi
    resized = to_be_resized.resize(newSize, resample=PIL.Image.BICUBIC)

    resized.save(filename)  # overwrite
    return pathlib.Path(filename).absolute()


def generate_barcodeset(short_ID,
                        n=config.settings['BARCODES'].getint('n_diff_bc'),
                        blank=config.settings['BARCODES'].getboolean('blank')):

    TARGET_DIR = os.path.join(config.BC_DIR, short_ID)
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    barcodes = []
    if blank:
        f = generate_barcode(short_ID, outdir=TARGET_DIR)
        barcodes.append(f)

    for i in range(n):
        bc = generate_barcode(short_ID + "-" + str(i + 1), outdir=TARGET_DIR)
        barcodes.append(bc)

    return barcodes


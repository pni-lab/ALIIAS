import barcode
from barcode.writer import ImageWriter
import PIL
from PIL import Image, ImageFont, ImageOps
import ALIIAS.config as config
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

    newSize = (config.settings['BARCODES'].getint('x_dim'),
               config.settings['BARCODES'].getint('y_dim'))  # for 38.1mmx19.05mm at 500dpi
    resized = to_be_resized.resize(newSize, resample=PIL.Image.BICUBIC)

    resized.save(filename)  # overwrite
    return pathlib.Path(filename).absolute()


def generate_barcode_set(short_ID,
                         n=config.settings['BARCODES'].getint('n_numbered_bc')):
    TARGET_DIR = os.path.join(config.BC_DIR, short_ID)
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    barcodes_path = []

    f = generate_barcode(short_ID, outdir=TARGET_DIR)
    barcodes_path.append(f)

    for i in range(n):
        bc = generate_barcode(short_ID + "-" + str(i + 1), outdir=TARGET_DIR)
        barcodes_path.append(bc)

    merged_path = merge_files_pdf(barcodes_path, short_ID)
    return merged_path


def merge_files_pdf(barcodes_path, short_ID, n_dups=config.settings['BARCODES'].getint('n_duplicate_bc')):
    TARGET_DIR = os.path.join(config.BC_DIR, short_ID)

    first_bc = ImageOps.expand(Image.open(barcodes_path[0]), border=40, fill='white')

    for i in range(n_dups):
        barcodes_path.append(barcodes_path[0])

    barcodes_path.pop(0)

    barcodes = []
    for bc_path in barcodes_path:
        barcodes.append(ImageOps.expand(Image.open(bc_path), border=40, fill='white'))

    path = pathlib.Path(TARGET_DIR).joinpath('barcode_' + short_ID + '_batch.pdf')
    first_bc.save(path, save_all=True, append_images=barcodes)
    return [path]

import barcode
from barcode.writer import ImageWriter
import PIL
from PIL import Image, ImageFont, ImageOps
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

    newSize = (config.settings['BARCODES'].getint('x_dim'), config.settings['BARCODES'].getint('y_dim'))  # for 38.1mmx19.05mm at 500dpi
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

    merged_path = merge_files_pdf(barcodes, short_ID)
    return merged_path

def merge_files_pdf(barcodes_path, short_ID, n=config.settings['BARCODES'].getint('n_diff_bc'),
                         dups=config.settings['BARCODES'].getint('n_identical_bc')):
    TARGET_DIR = os.path.join(config.BC_DIR, short_ID)

    first_bc = ImageOps.expand(Image.open(barcodes_path[0]), border=40, fill='white')

    for i in range(dups-1):
        barcodes_path.append(barcodes_path[0])

    barcodes_path.pop(0)

    barcodes = []
    for bc_path in barcodes_path:
        barcodes.append(ImageOps.expand(Image.open(bc_path), border=40, fill='white'))

    path = pathlib.Path(TARGET_DIR).joinpath('barcode_' + short_ID + '_batch.pdf')
    first_bc.save(path, save_all=True, append_images=barcodes)
    return [path]


def merge_files_png(barcodes, short_ID,
                         n=config.settings['BARCODES'].getint('n_diff_bc'),
                         dups=config.settings['BARCODES'].getint('n_identical_bc')):
    TARGET_DIR = os.path.join(config.BC_DIR, short_ID)
    width = config.settings['BARCODES'].getint('x_dim')
    height = config.settings['BARCODES'].getint('y_dim')
    space = config.settings['BARCODES'].getint('label_gap')

    target = Image.new('RGB', (width, (n+dups + 1) * height + (n+dups-1) * space), color=(255, 255, 255))

    for i in range(dups-1):
        barcodes.append(barcodes[0])

    for idx, bc in enumerate(barcodes):
        target.paste(Image.open(bc), (0, idx * (height + space)))

    for i in range(dups-1):
        barcodes.pop(-1)

    path = pathlib.Path(TARGET_DIR).joinpath('barcode_' + short_ID + '_total.png')
    target.save(path)
    return [path]

import barcode
from barcode.writer import ImageWriter
import PIL
from PIL import Image

writer = ImageWriter()
barcode = barcode.get('code128', '32d5h60a', writer=writer)
filename = barcode.save('barcode_test',
                        {"module_width": 38.1/110,
                         "module_height": 19.05,
                         "text_distance": 1.0,
                         "font_size": 40})


to_be_resized = Image.open(filename)
newSize = (750, 375)  # for 38.1mmx19.05mm at 500dpi
resized = to_be_resized.resize(newSize, resample=PIL.Image.BICUBIC)

resized.save('barcode_test3.png')
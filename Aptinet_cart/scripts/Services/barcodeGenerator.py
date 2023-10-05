from PySide2.QtQuick import *
import code128
from PIL import Image


class BarcodeGenerator(QQuickImageProvider):
    def __init__(self):
        super().__init__(QQuickImageProvider.Image)

    def requestImage(self,url, p_str, size):
        barcode_param = url[3:-3]

        barcode_image = code128.image(barcode_param, height=100)
        w, h = barcode_image.size
        margin = 20
        new_h = h +(2*margin) 

        new_image = Image.new('RGBA', (w, new_h), (255, 255, 255))

        new_image.paste(barcode_image, (0, margin))
        im = new_image.toqimage()
        return im

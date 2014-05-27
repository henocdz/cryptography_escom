from PIL import Image
import os
import tempfile


class CryptoImage(object):

    def __init__(self):
        self.colors = []
        self.str_colors = ''

    def load_image_from_string(self, str, size):
        self.str_colors = str
        self.size = size
        self.colors = self._string_to_colors()

    def load_image(self, fail):
        self.file = fail
        self._init_colors()

    def get_colors_as_string(self):
        return self._colors_to_string()

    def save(self, size=None):
        i = Image.new("RGB", self.size)
        irgb = i.convert("RGB", palette=Image.ADAPTIVE)

        self.colors = (
            self.colors if type(self.colors) is tuple
            else self._colors_to_tuple()
        )

        irgb.putdata(self.colors)
        img_obj, img_path = tempfile.mkstemp(suffix='.bmp')
        irgb.save(img_path)
        self.path = img_path

    def delete(self):
        os.remove(self.path)

    def _colors_to_tuple(self):
        return tuple([tuple(color) for color in self.colors])
        # print self.colors

    def _init_colors(self):
        i = Image.open(self.file)
        irgb = i.convert("RGB", palette=Image.ADAPTIVE)
        colors = list(irgb.getdata())
        self.colors = colors
        self.size = i.size

    def _colors_to_string(self):
        colors = self.colors
        return ''.join([chr(rgb) for color in colors for rgb in color])

    def _string_to_colors(self):
        """Convert string of chars into pixels format RGB"""
        string = self.str_colors
        colors_three = [string[c:c+3] for c in range(0, len(string), 3)]
        colors_three = [list(color) for color in colors_three]
        pixels = [[ord(rgb) for rgb in color] for color in colors_three]
        return pixels

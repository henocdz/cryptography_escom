from numpy import matrix as _matrix
from numpy import linalg as _linalg
import Tkinter as tk
import tkFileDialog
import tkSimpleDialog
import os, sys, numpy, time
from PIL import Image

root = tk.Tk()
ROOT_WIDTH = root.winfo_screenwidth()
ROOT_HEIGHT = root.winfo_screenheight()

root.title('Hill Cipher v0.1')

class ImageCipher(tk.Frame):
    btn_file, btn_decrypt = None, None
    KEY = [[1,2,3],[4,5,6],[11,9,8]]
    KEY_INVERSE = [[90,167,1],[74,179,254],[177,81,1]]

    def hill_cipher(self, matrix, key):
        a = _matrix(matrix)
        k = _matrix(key)
        a_k = a*k
        a_k = a_k.tolist()
        return a_k[0]

    def xor(self, icolor, ocolor):
        il = len(icolor)

        res = []
        for i in range(0,il):
            res.append(icolor[i]^ocolor[i])
        return res

    def mod(self, color):
        r, g, b = color
        while r > 255:
            r = r % 256
        while g > 255:
            g = g % 256
        while b > 255:
            b = b % 256

        return (r,g,b)

    def encrypt(self, colors, key):
        encrypted = []
        prevcolor = [0, 0, 0]
        i = 0
        for color in colors:
            if i < 99:
                print prevcolor, color , self.xor(prevcolor, color)
            i+=1
            
            color_ = self.xor(color, prevcolor)
            clr = self.mod(self.hill_cipher(color_, key))
            prevcolor = clr
            encrypted.append(self.mod(clr))
        return encrypted

    def decrypt(self, colors, ikey):
        decrypted = []
        prevcolor = [0,0,0]
        for color in colors:
            clr = self.mod(self.hill_cipher(color, ikey))
            color_ = self.xor(clr, prevcolor)
            prevcolor = color

            decrypted.append(tuple(color_))

        return decrypted

    def _decrypt(self, files):
        z = 256

        for _file in files:
            i = Image.open(_file)
            ext = self._getFormat(_file)
            irgb = i.convert("RGB", palette=Image.ADAPTIVE)
            colors = list(irgb.getdata())
            colors_decrypted = self.decrypt(colors,self.KEY_INVERSE)

            irgb.putdata(colors_decrypted)
            path = '/'.join(_file.split('/')[:-1])
            ts = time.time()
            irgb.save("%s/restored_%d.%s" % (path,int(ts),  ext) )
            print "Guardada"

    def _encrypt(self, files):
        z = 256

        for _file in files:
            i = Image.open(_file)
            ext = self._getFormat(_file)
            irgb = i.convert("RGB", palette=Image.ADAPTIVE)
            colors = list(irgb.getdata())
            colors_encrypted = self.encrypt(colors, self.KEY)

            irgb.putdata(colors_encrypted)
            path = '/'.join(_file.split('/')[:-1])
            ts = time.time()
            irgb.save("%s/output_%d.%s" % (path,int(ts),ext) )
            print "Guardada \n >>>>> "

    def _getFormat(self, _file):
        return _file.split('.')[-1]

    def createWidgets(self):
        def e_openchooser():
            _file = tkFileDialog.askopenfilenames(
                filetypes =
                    [
                        ('Images', '.jpg'),
                        ('Images', '.png'), 
                        ('Images', '.bmp'), 
                    ],
                initialdir = "/home/henocdz/Escritorio",
                multiple = False,
                title = "Choose an Image to encrypt :)"
            )

            self._encrypt(_file)

        def e_openchooser_decrypt():
            _file = tkFileDialog.askopenfilenames(
                filetypes =
                    [
                        ('Images', '.jpg'),
                        ('Images', '.png'), 
                        ('Images', '.bmp'), 
                    ],
                initialdir = "/home/henocdz/Escritorio",
                multiple = False,
                title = "Choose an Image to decrypt :)"
            )

            self._decrypt(_file)

        self.btn_file = tk.Button(self,  text="Open Image to Encrypt", command=e_openchooser)
        self.btn_file.grid()

        self.btn_decrypt = tk.Button(self, text="Open Image to Decrypt", command=e_openchooser_decrypt)
        self.btn_decrypt.grid()

    def __init__(self, master=None, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.pack(fill=None,expand=False,side=tk.RIGHT)
        self.place(relx=.5, rely=.5, anchor="c")
        self.createWidgets()

frame = ImageCipher(root, width=ROOT_WIDTH/2, height=ROOT_HEIGHT/2)

root.pack_propagate(0)
root.mainloop()




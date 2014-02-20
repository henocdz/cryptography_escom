import Tkinter as tk
import tkFileDialog
import tkSimpleDialog
import os, sys, numpy, time
from PIL import Image
root = tk.Tk()
ROOT_WIDTH = root.winfo_screenwidth()
ROOT_HEIGHT = root.winfo_screenheight()

root.title('Image Cipher v0.1')

class EuclideanAlgorithm:
	def __init__(self):
		pass

	def modinverse(self, a, b):
		g, x, y = self.egcd(a, b)
		if g != 1:
			return None  # modular inverse does not exist
		else:
			return x % m

	def egcd(self, a, b):
		if a == 0:
			return (b, 0, 1)
		else:
			g, y, x = self.egcd(b % a, a)
			return (g, x - (b // a) * y, y)

class ImageCipher(tk.Frame):
	btn_file, btn_decrypt = None, None

	def _getColorShift(self,color_txt='?', error_txt=''):
		t = "%s \n Set %s shift: " % (error_txt, color_txt)
		tt = "Set %s shift: " % color_txt
		color =  tkSimpleDialog.askinteger(tt, t)

		try:
			color = int(color)
		except:
			print "Hey! %s is not a number." % color
			e = "Hey! %s is not a number." % color
			color = self._getColorShift(color_txt=color_txt,error_txt=e)
		
		if color > 255 or color < 0:
			print "%s is not a valid value. MUST be between 0 and 255" % color
			e = "%s is not a valid value. MUST be between 0 and 255" % color
			color = self._getColorShift(color_txt=color_txt, error_txt=e)			
		
		return color

	def _getShift(self):
		ru = self._getColorShift(color_txt="R")
		gu = self._getColorShift(color_txt="G")
		bu = self._getColorShift(color_txt="B")
		return ru,gu,bu

	def _shift(self, colors, betar, betag, betab):
		colors_= []
		for i in range(0, 5):
			print "pre>> " + str(colors[i])

		print "-------------"
		for color in colors:
			r, g, b = color
			r, g, b = r+betar, g+betag, b+betab

			while r > 255:
				r = r % 256
			while g > 255:
				g = g % 256
			while b > 255:
				b = b % 256

			colors_.append((r,g,b))

		for i in range(0, 5):
			print "pos>> " + str(colors_[i])

		return colors_

	def _decrypt(self, files):
		z = 256
		ru,gu,bu = self._getShift()

		for _file in files:
			i = Image.open(_file)
			ext = self._getFormat(_file)
			irgb = i.convert("RGB", palette=Image.ADAPTIVE)
			colors = list(irgb.getdata())
			colors_decrypted = self._shift(colors, (z - ru), (z - gu), (z - bu))

			irgb.putdata(colors_decrypted)
			path = '/'.join(_file.split('/')[:-1])
			ts = time.time()
			irgb.save("%s/restored_%d.%s" % (path,int(ts),  ext) )
			print "Guardada"

	def _encrypt(self, files):
		z = 256
		ru,gu,bu = self._getShift()

		for _file in files:
			i = Image.open(_file)
			ext = self._getFormat(_file)
			irgb = i.convert("RGB", palette=Image.ADAPTIVE)
			colors = list(irgb.getdata())
			colors_encrypted = self._shift(colors, ru, gu, bu)

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

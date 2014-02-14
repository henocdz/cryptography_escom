import Tkinter as tk
import tkFileDialog
import os, sys, numpy
from PIL import Image
root = tk.Tk()
ROOT_WIDTH = root.winfo_screenwidth()
ROOT_HEIGHT = root.winfo_screenheight()

root.title('Image Cipher v0.1')


class ImageCipher(tk.Frame):
	btn_file = None

	def _getColorShift(self,color_txt):
		color = raw_input("Set %s shift: " % color_txt)

		try:
			color = int(color)
		except:
			print "Hey! %s is not a number." % color
			color = self._getColorShift(color_txt)

		if color > 255 or color < 0:
			print "%s is not a valid value. MUST be between 0 and 255" % color
			color = self._getColorShift(color_txt)			

		return color

	def fileChoosen(self, files):
		ru = self._getColorShift("R")
		gu = self._getColorShift("B")
		bu = self._getColorShift("G")

		for _file in files:
			i = Image.open(_file)
			irgb = i.convert("RGB")
			#print irgb.getdata()
			colors = list(irgb.getdata())
			colors_encrypted = []
			
			for color in colors:
				r,g,b = color
				r, g, b = r+ru, g+gu, b+bu

				while r > 255:
					r = r % 256

				while g > 255:
					g = g % 256

				while b > 255:
					b = b % 256

				colors_encrypted.append((r,g,b))

			irgb.putdata(colors_encrypted)
			#for c in range(5):
				#print colors_encrypted[c], colors[c]

			#o = Image.fromarray(colors_encrypted)
			irgb.save('output.jpg')

	def createWidgets(self):
		def e_openchooser():
			_file = tkFileDialog.askopenfilenames(
				filetypes =
					[
						#('Images', '.jpg,.png'),
						('JPG Image', '.jpg'),
						('PNG Image', '.png'), 
					],
				initialdir = "/home/henocdz/Escritorio",
				multiple = False,
				title = "Choose an Image to encrypt :)"
			)

			self.fileChoosen(_file)

		self.btn_file = tk.Button(self,  text="Open Image", command=e_openchooser)
		self.btn_file.pack(side=tk.LEFT)

	def __init__(self, master=None, *args, **kwargs):
		tk.Frame.__init__(self, master, *args, **kwargs)
		self.pack(side=tk.RIGHT)
		self.createWidgets()

#frame = tk.Frame(root, width=ROOT_WIDTH/2, height=ROOT_HEIGHT/2)

frame = ImageCipher(root, width=ROOT_WIDTH/2, height=ROOT_HEIGHT/2)

#frame.pack(side=tk.TOP)
root.mainloop()

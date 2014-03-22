from PIL import Image
from zipfile import ZipFile
import tempfile
import os

def create_zip():
    pass

def mod(data, z):
    rdata = []
    for d in data:
        aux = d
        if type(d) is str or type(d) is unicode:
            aux = ord(d)

        while aux > z:
            aux = aux%z
        rdata.append(aux)
    return tuple(rdata)

def file_format(_file):
    return _file.name.split('.')[-1]

def get_colors(_file):
    i = Image.open(_file)
    irgb = i.convert("RGB", palette=Image.ADAPTIVE)
    colors = list(irgb.getdata())

    return colors, i.size

def save_image(colors,size):
    i = Image.new("RGB",size)
    irgb = i.convert("RGB", palette=Image.ADAPTIVE)
    irgb.putdata(colors)
    img_obj, img_path = tempfile.mkstemp(suffix='.bmp')
    irgb.save(img_path)
    return img_path

def create_zip(paths, filename, ext):
    zip_obj, zip_path = tempfile.mkstemp(suffix='.zip')    
    _zip = ZipFile(zip_path, 'w')
        
    for i,path in enumerate(paths):
        _zip.write(path, "%s_%d.%s" %(filename,i,ext))
        os.remove(path)

    _zip.close()

    return zip_path
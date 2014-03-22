from PIL import Image

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
    path = "/tmp/output_.bmp" 
    irgb.save(path)
    return path
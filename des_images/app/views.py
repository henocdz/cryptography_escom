from flask import render_template, request, make_response
from app import app
from . import forms
import os
from Crypto.Cipher import DES
from .tools import create_zip
from .cryptoimage import CryptoImage
from Crypto.Util import Counter

BASE_DIR = os.path.dirname(__file__)
OP_MODES = {
    'ecb': DES.MODE_ECB, 'cbc': DES.MODE_CBC,
    'cfb': DES.MODE_CFB, 'ofb': DES.MODE_OFB,
    'ctr': DES.MODE_CTR
}
IV = "12345678"

@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def encrypt():  # Verify

    eform = forms.ImageForm()

    if eform.validate_on_submit():
        encrypt = eform.encrypt.data
        image = request.files['image']
        password = eform.password.data
        op_mode = eform.op_mode.data
        op_mode = OP_MODES[op_mode] if op_mode in OP_MODES else OP_MODES['ecb']

        img = CryptoImage()
        img.load_image(image)

        chunks = chunker(img.get_colors_as_string())

        if encrypt:
            imgs_encrypted = encrypt_all(chunks, password, img.size)
            paths = [i.path for i in imgs_encrypted]

            zipath = create_zip(paths)
            zep = open(zipath)

            res = make_response(zep.read())
            res.headers['Content-Disposition'] = 'attachment; filename="%s_encrypted.zip"' %  ''

            return res
        else:
            img_decrypted = decrypt(chunks, password, op_mode, img.size)
            img = open(img_decrypted.path)
            res = make_response(img.read())
            res.headers['Content-Disposition'] = 'attachment; filename="%s_encrypted.bmp"' %  ''

            return res

    return render_template('index.html', form=eform)


def decrypt(data, password, mode, img_size):
    cipher = DES.new(password, mode, IV)
    image_data = []
    image = CryptoImage()

    for d in data:
        image_data.append(cipher.decrypt(d))

    image.load_image_from_string(''.join(image_data), img_size)
    image.save()

    return image


def encrypt_all(data, password, img_size):
    ciphers = [
        DES.new(password, DES.MODE_ECB, IV),
        DES.new(password, DES.MODE_CBC, IV),
        DES.new(password, DES.MODE_CFB, IV),
        DES.new(password, DES.MODE_OFB, IV),
        # DES.new(password, DES.MODE_CTR, '12345678', Counter)
    ]
    encrypted = []
    for cipher in ciphers:
        image_data = []
        image = CryptoImage()
        for d in data:
            image_data.append(cipher.encrypt(d))

        image.load_image_from_string(''.join(image_data), img_size)
        image.save()
        encrypted.append(image)

    return encrypted


def chunker(string):
    chunks = [string[s:s+8] for s in range(0, len(string), 8)]
    return chunks

if __name__ == '__main__':
    app.run()

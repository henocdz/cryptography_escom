from flask import render_template, request, make_response
from .tools import create_zip, chunker
from .cryptoimage import CryptoImage
from Crypto.Util import Counter
from Crypto.Cipher import DES
from . import forms
from app import app
import os

BASE_DIR = os.path.dirname(__file__)
OP_MODES = {
    'ecb': DES.MODE_ECB, 'cbc': DES.MODE_CBC,
    'cfb': DES.MODE_CFB, 'ofb': DES.MODE_OFB,
    'ctr': DES.MODE_CTR
}
IV = "12345678"
BLOCK_SIZE_BITS = 64


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

            zep.close()
            os.remove(zipath)

            res.headers['Content-Disposition'] = 'attachment; filename="%s_encrypted.zip"' %  ''

            return res
        else:
            img_decrypted = decrypt(chunks, password, op_mode, img.size)
            img = open(img_decrypted.path)
            res = make_response(img.read())

            img.close()
            os.remove(img_decrypted.path)

            res.headers['Content-Disposition'] = 'attachment; filename="%s_encrypted.bmp"' %  ''

            return res

    return render_template('index.html', form=eform)


def decrypt(data, password, mode, img_size):

    if mode == DES.MODE_CTR:
        cipher = DES.new(password, mode, IV, Counter.new(BLOCK_SIZE_BITS))
    else:
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
        DES.new(password, DES.MODE_CTR, IV, Counter.new(BLOCK_SIZE_BITS))
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

if __name__ == '__main__':
    app.run()

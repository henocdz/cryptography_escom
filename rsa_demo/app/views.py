from flask import render_template
from app import app
from . import forms
import os
from urllib import urlopen
from M2Crypto import RSA, BIO

BASE_DIR = os.path.dirname(__file__)
PUBLIC_KEY = os.path.join(BASE_DIR, 'static/pub.key')
PRIVATE_KEY = os.path.join(BASE_DIR, 'static/priv.key')


@app.route('/pubkey')
def public_key():
    pub = open(PUBLIC_KEY).read()
    return pub


@app.route('/privkey')
def private_key():
    pub = open(PRIVATE_KEY).read()
    return pub


@app.route('/')
@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():  # Verify

    eform = forms.EncryptForm()
    encrypted = None
    if eform.validate_on_submit():
        rsa = load_public_key(
            eform.from_url.data, eform.e.data, eform.n.data, eform.url.data
        )

        if rsa:
            encrypted = pencrypt(rsa, eform.message.data)

    return render_template('encrypt.html', form=eform, cipher_text=encrypted)


@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    eform = forms.EncryptForm()
    encrypted = None
    if eform.validate_on_submit():
        rsa = load_private_key(
            eform.from_url.data,  eform.url.data
        )

        if rsa:
            encrypted = pdecrypt(rsa, eform.message.data)

    return render_template('decrypt.html', form=eform, cipher_text=encrypted)


# Tools
def load_public_key(from_url=False, e=None, n=None, url=None):

    if url and from_url:
        try:
            key_str = urlopen(url).read()
            bio = BIO.MemoryBuffer(key_str)
            key = RSA.load_pub_key_bio(bio)
        except IOError:
            key = None
    elif e and n:
        key = RSA.new_pub_key((e, n))
    else:
        key = None

    return key


def load_private_key(from_url=False, url=None):

    if url and from_url:
        try:
            key_str = urlopen(url).read()
            bio = BIO.MemoryBuffer(key_str)
            key = RSA.load_key_bio(bio)
        except IOError:
            key = None
    else:
        key = None

    return key

DEC_CHUCK_SIZE = 29
HEX_CHUNK_SIZE = 256


def pencrypt(cipher, data):

    ldata = len(data)

    if ldata <= DEC_CHUCK_SIZE:
        return cipher.public_encrypt(data, RSA.pkcs1_padding).encode('hex')
    else:
        chunks = chunker(data, DEC_CHUCK_SIZE)
        chunks_en = []
        for chunk in chunks:
            chunks_en.append(
                cipher.public_encrypt(chunk, RSA.pkcs1_padding).encode('hex')
            )

        return ''.join(chunks_en)


def pdecrypt(cipher, data):
    ldata = len(data)

    if ldata <= HEX_CHUNK_SIZE:
        data = data.decode('hex')
        return cipher.private_decrypt(data, RSA.pkcs1_padding)
    else:
        chunks = chunker(data, HEX_CHUNK_SIZE)
        chunks_de = []
        for chunk in chunks:
            chunks_de.append(cipher.private_decrypt(
                chunk.decode('hex'), RSA.pkcs1_padding)
            )

        return ''.join(chunks_de)


def chunker(data, MAX_CHUCK_SIZE=29):
    chunks = []
    ldata = len(data)

    for inicio in range(0, ldata, MAX_CHUCK_SIZE):
        fin = inicio + MAX_CHUCK_SIZE if (inicio + MAX_CHUCK_SIZE) < ldata else ldata
        print fin, inicio
        chunks.append(data[inicio:fin])

    return chunks

if __name__ == '__main__':
    app.run()

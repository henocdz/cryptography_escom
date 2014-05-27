from flask import render_template, make_response, request
from app import app
from . import forms
import os
from urllib import urlopen
from M2Crypto import RSA, BIO, EVP
import hashlib
import binascii

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
@app.route('/verify', methods=['GET', 'POST'])
def verify():  # Verify

    eform = forms.VerifyForm()
    verified = None
    if eform.validate_on_submit():
        fail = request.files['message']
        data, sign = getdata(fail)

        rsa = load_public_key(eform.from_url.data, eform.url.data)

        if rsa:
            pubkey = EVP.PKey()
            pubkey.assign_rsa(rsa)
            pubkey.verify_init()
            pubkey.verify_update(data)
            verified = pubkey.verify_final(sign)
            print verified

    return render_template('encrypt.html', form=eform, sign_text=verified)


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    eform = forms.EncryptForm()
    signature = None
    if eform.validate_on_submit():

        rsa = load_private_key(eform.from_url.data, eform.url.data)

        if rsa:
            pkey = EVP.PKey()
            pkey.assign_rsa(rsa)
            pkey.sign_init()
            pkey.sign_update(eform.message.data)
            signature = binascii.b2a_hex(pkey.sign_final())

            txt = gentxt(eform.message.data, signature)
            res = make_response(txt)
            res.headers['Content-Disposition'] = "attachment; filename=signed.txt"

            return res

    return render_template('decrypt.html', form=eform, sign_text=signature)


def gentxt(data, sign):
    res = """%s\nSIGN:\n%s""" % (data, sign)
    return res


def getdata(fail):
    mark_length = 5
    data = ''
    sign = ''
    file_data = fail.read()
    sign_x = file_data.find('SIGN:')
    data = unicode(file_data[0:sign_x].strip('\n').strip())
    sign = binascii.a2b_hex(file_data[sign_x+mark_length:].strip('\n').strip())
    print repr(data), repr(sign)
    return data, sign


# Tools
def load_public_key(from_url=False, url=None):

    if url and from_url:
        try:
            key_str = urlopen(url).read()
            bio = BIO.MemoryBuffer(key_str)
            key = RSA.load_pub_key_bio(bio)
        except IOError:
            key = None
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


if __name__ == '__main__':
    app.run()

from flask import render_template
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

    eform = forms.EncryptForm()
    verified = None
    if eform.validate_on_submit():
        sign = binascii.a2b_hex(eform.signature.data)

        rsa = load_public_key(
            eform.from_url.data, eform.url.data
        )

        if rsa:
            pubkey = EVP.PKey()
            pubkey.assign_rsa(rsa)
            pubkey.verify_init()
            pubkey.verify_update(eform.message.data)
            verified = pubkey.verify_final(sign)

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

    return render_template('decrypt.html', form=eform, sign_text=signature)


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

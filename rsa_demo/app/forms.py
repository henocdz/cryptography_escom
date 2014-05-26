from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextField, TextAreaField
from wtforms.validators import Required, URL


class EncryptForm(Form):
    e = StringField('e')
    n = StringField('n')
    url = StringField('URL public key in b64')
    from_url = BooleanField('PubKey Base64', default=True)
    message = TextAreaField('Message to encrypt', validators=[Required()])

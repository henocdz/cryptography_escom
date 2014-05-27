from flask.ext.wtf import Form
from wtforms import BooleanField, SelectField, FileField, PasswordField
from wtforms.validators import Required


class ImageForm(Form):
    image = FileField(validators=[Required()])
    password = PasswordField(validators=[Required()])
    encrypt = BooleanField(default=True)
    op_mode = SelectField(choices=[
        ('ecb', 'ECB'), ('cbc', 'CBC'),
        ('cfb', 'CFB'), ('ofb', 'OFB'), ('ctr', 'CTR')
    ])

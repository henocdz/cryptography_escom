from flask import Flask
from flask_wtf.csrf import CsrfProtect

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    CSRF_ENABLED=True,
    SECRET_KEY='1224567865432'
)

CsrfProtect(app)

from app import views

from flask import Flask


app = Flask (__name__)
app.secret_key = "SecretKey"

from flask_app.controllers import inputs
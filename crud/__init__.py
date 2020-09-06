from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key= "b'\xb2<\xb0\xdc\xad\x12K\x85\xffj\xe7\x91\x8d\x95\x03Q\x9e\x98\xec.\xdb\x1bk'"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_BINDS'] = {'postdb':'sqlite:///postdb.db',
                                   'users' : 'sqlite:///users.db'}

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)

from crud import routes, models
from datetime import datetime, date, time
from crud import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired
from wtforms.fields.html5 import TelField

# Main database


class main(db.Model):
    id = db.Column(db.Integer, primary_key=True)
# Users database


class users(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(300))
    name = db.Column(db.String(300))
    number = db.Column(db.String(300))
    password = db.Column(db.String(80))

    def __init__(self, username, email, name, number, password):
        self.username = username
        self.email = email
        self.name = name
        self.number = number
        self.password = password


# Posts database
class postdb(db.Model):
    __bind_key__ = 'postdb'
    today = datetime.now().strftime('%y%b%d').upper()
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date_posted = db.Column(db.String, default=today)
    author = db.Column(db.String(100))
    content = db.Column(db.Text)

    def __init__(self, title, author, content):
        self.title = title
        self.author = author
        self.content = content

# Forms


class loginForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired()])
    name = StringField('Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    phone = StringField('Phone Number', validators=[InputRequired()])

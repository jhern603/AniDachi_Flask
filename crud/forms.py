from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, TextAreaField, SelectField, HiddenField, BooleanField
from wtforms.validators import ValidationError, Length, EqualTo, DataRequired
from crud.models import users

# Register form manager


class register_form(FlaskForm):
    id = HiddenField('id')
    email = StringField('E-mail', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])

    def validate_username(self, username):
        user = users.query.filter_by(username=username.data).first()
        if user:
            flash('This user already exists.')

# Login form manager


class login_form(FlaskForm):
    id = HiddenField('id')
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me.', validators=[DataRequired()])


# Edit User form manager
class edit_user_form(FlaskForm):
    id = HiddenField('id')
    email = StringField('E-mail', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password')
    phone = StringField('Phone Number', validators=[DataRequired()])

# Post form manager


class post_form(FlaskForm):
    id = HiddenField('id')
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author')
    content = StringField('Post content', validators=[DataRequired()])

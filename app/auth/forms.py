from wtforms import validators as vl
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf import FlaskForm

from ..models import User


# TODO add email checking regexp
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        vl.DataRequired(),
        vl.Length(1, 64),
        vl.Email(),
    ])
    password = PasswordField('Password', validators=[vl.DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        vl.DataRequired(),
        vl.Length(1, 64),
        vl.Email()
    ])
    username = StringField('Username', validators=[
        vl.DataRequired(),
        vl.Length(1, 64),
        vl.Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                  message='Usernames must contain only letters, numbers, dots, or underscores')
    ])
    password = PasswordField('Password', validators=[
        vl.DataRequired(),
        vl.EqualTo('password2', 'Passwords must match.'),
    ])
    password2 = PasswordField('Confirm password', validators=[vl.DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise vl.ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise vl.ValidationError('Username is already in use.')

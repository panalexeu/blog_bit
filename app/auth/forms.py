import wtforms as wtf
from wtforms import validators as vl
from flask_wtf import FlaskForm


# TODO add email checking regexp
class LoginForm(FlaskForm):
    email = wtf.StringField('Email', validators=[
        vl.DataRequired(),
        vl.Length(1, 64),
        vl.Email(),
    ])
    password = wtf.PasswordField('Password', validators=[vl.DataRequired()])
    remember_me = wtf.BooleanField('Keep me logged in')
    submit = wtf.SubmitField('Log In')

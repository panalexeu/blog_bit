from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, SelectField, ValidationError
from wtforms import validators as vl
from flask_pagedown.fields import PageDownField

from ..models import User
from ..models import Role


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[vl.Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(EditProfileForm):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.default).all()]

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
    role = SelectField('Role', coerce=int)
    confirmed = BooleanField('Confirm status')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?")
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    body = StringField('What do you think?', validators=[vl.DataRequired()])
    submit = SubmitField('Submit')

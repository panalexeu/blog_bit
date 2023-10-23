from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, SelectField, ValidationError
from wtforms import validators as vl

from ..models import Role, User


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
    confirmed = BooleanField('Confirm status')
    role = SelectField('Role', coerce=int)
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')

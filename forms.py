from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, TextAreaField, validators

from validators import NoProfanity


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25),
                                        validators.Regexp(r'^[a-zA-Z0-9_\.]+$',
                                                          message='Only letters, numbers, underscore character and dots are allowed.'),
                                        validators.Regexp(r'^[a-zA-Z0-9]+([._]?[a-zA-Z0-9]+)*$',
                                                          message='Dots and underscores cannot be at the start of the username, repeat or touch.'),
                                        NoProfanity()])
    name = StringField('Name', [validators.Length(min=2, max=35), NoProfanity()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = StringField('Password', [validators.DataRequired()])
    remember_me = BooleanField('Remember Me', [validators.Optional()])


class EditProfileForm(FlaskForm):
    name = RegistrationForm.name
    about_me = TextAreaField('About Me', [validators.Optional(), NoProfanity()], description='Tell us about yourself', )


class NewPostForm(FlaskForm):
    text = TextAreaField('Text', [validators.Length(min=15, max=1000), NoProfanity()], description='Express yourself.')


class NewCommentForm(FlaskForm):
    text = StringField('Text', [validators.Length(min=1, max=50), NoProfanity()])

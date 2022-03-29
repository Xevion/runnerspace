from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    name = StringField('Name', [validators.Length(min=2, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = StringField('Password', [validators.DataRequired()])
    remember_me = BooleanField('Remember Me', [validators.Optional()])


class EditProfileForm(Form):
    name = RegistrationForm.name
    about_me = StringField('About Me', [validators.Optional()])


class NewPostForm(Form):
    text = StringField('Text', [validators.Length(min=15, max=1000)])


class NewCommentForm(Form):
    text = StringField('Text', [validators.Length(min=5, max=50)])

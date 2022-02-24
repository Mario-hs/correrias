from wtforms import Form, BooleanField, StringField, PasswordField, validators

class LoginForm(Form):
    username = StringField('username', [validators.data_required()])
    password = PasswordField('password', [validators.data_required()])
    remember_me = BooleanField('remember_me')


class RegisterForm(Form):
    username = StringField('username', [validators.data_required(), validators.Length(min=4, max=25)])
    password = PasswordField('password', [validators.data_required(), validators.Length(min=4, max=25)])
    email = StringField('email', [validators.data_required(), validators.Length(min=10, max=35)])
    cnpj = StringField('cnpj', [validators.data_required(), validators.Length(min=14, max=14)])
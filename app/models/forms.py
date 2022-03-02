from tkinter.tix import Select
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class LoginForm(Form):
    name = StringField('name', [validators.data_required()])

    password = PasswordField('password', [validators.data_required()])

    remember_me = BooleanField('remember_me')


class RegisterForm(Form):
    name = StringField('name', [validators.data_required(), validators.Length(min=4, max=25)])

    password = PasswordField('password', [validators.data_required(), validators.Length(min=4, max=25)])

    email = StringField('email', [validators.data_required(), validators.Length(min=10, max=35)])

    cnpj = StringField('cnpj', [validators.data_required(), validators.Length(min=14, max=14)])

class PackageRegisterForm(Form):
    name = StringField('name', [validators.data_required(), validators.Length(min=4, max=25)])

    cpf = StringField('cpf', [validators.data_required(), validators.Length(min=11, max=11)])

    email = StringField('email', [validators.data_required(), validators.Length(min=10, max=25)])

    id_pack = StringField('id_pack', [validators.data_required(), validators.Length(min=12, max=12)])

    weight = StringField('weight', [validators.data_required(), validators.Length(min=1, max=5)])

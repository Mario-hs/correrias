from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate
# from app.models import db
from flask_login import LoginManager

app = Flask(__name__)
# app.config['SQLALCHEMY_DATA_URI']='sqlite:////storage.sqlite'
app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
# manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)


from app.models import db, forms
from app.controllers import default

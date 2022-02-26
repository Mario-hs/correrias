import os
DEBUG = True

# SQLALCHEMY_DATA_URI = 'sqlite:///' + os.path.join(basedir, 'storage.sqlite')
SQLALCHEMY_DATA_URI = 'sqlite:////storage.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'secuty-password'
from flask import Flask


app = Flask(__name__)


from app.models import db, forms
from app.controllers import default


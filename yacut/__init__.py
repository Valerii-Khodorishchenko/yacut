from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Congig


app = Flask(__name__, static_folder='static')
app.config.from_object(Congig)
db = SQLAlchemy(app)
from .models import URLMap

with app.app_context():
    db.create_all()

from . import views
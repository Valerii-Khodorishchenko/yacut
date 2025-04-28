from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Config


app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
from .models import URLMap

with app.app_context():
    db.create_all()

from . import api_views, error_handlers, views
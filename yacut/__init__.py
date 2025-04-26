from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import Congig

app = Flask(__name__)
app.config.from_object(Congig)
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

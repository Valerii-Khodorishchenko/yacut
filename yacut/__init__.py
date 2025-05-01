from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

from settings import Config

SWAGGER_URL = '/api/docs'
API_DOCS_URI = '/static/docs/openapi.yml'
TITLE_API_DOCS = 'YaCut API Docs'

app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_DOCS_URI,
    config={'app_name': TITLE_API_DOCS}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

from . import api_views, error_handlers, views

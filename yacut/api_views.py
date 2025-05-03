from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


API_ERROR_REQUIRED = '"url" является обязательным полем!'
API_ERROR_NO_BODY = 'Отсутствует тело запроса'
API_ERROR_ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(API_ERROR_NO_BODY)
    if 'url' not in data:
        raise InvalidAPIUsage(API_ERROR_REQUIRED)
    original = data['url']
    short = data.get('custom_id')
    try:
        url_map = URLMap.create(original, short)
    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    except RuntimeError as e:
        raise InvalidAPIUsage(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short>/', methods=['GET'])
def get_original(short):
    if not (url_map := URLMap.get_or_false(short)):
        raise InvalidAPIUsage(API_ERROR_ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK

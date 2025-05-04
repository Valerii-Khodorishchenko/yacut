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
    try:
        return jsonify(
            URLMap.create(data['url'], data.get('custom_id')).to_dict()
        ), HTTPStatus.CREATED
    except ValueError as e:
        raise InvalidAPIUsage(str(e))
    except RuntimeError as e:
        raise InvalidAPIUsage(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


@app.route('/api/id/<short>/', methods=['GET'])
def get_original(short):
    if not (url_map := URLMap.get(short)):
        raise InvalidAPIUsage(API_ERROR_ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK

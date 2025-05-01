import re
from http import HTTPStatus

from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from . import app
from .constants import CHARSET, MAX_SHORT_LENGTH, MESSAGE_SHORT_TAKEN
from .error_handlers import InvalidAPIUsage
from .models import URLMap


SHORT_PATTERN = re.compile(rf'^[{CHARSET}]*$')
API_ERROR_REQUIRED = '"url" является обязательным полем!'
API_ERROR_NO_BODY = 'Отсутствует тело запроса'
API_ERROR_INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
API_ERROR_ID_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def create_url_map():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(API_ERROR_NO_BODY)
    if (original := data.get('url')) is None:
        raise InvalidAPIUsage(API_ERROR_REQUIRED)
    short = data.get('custom_id', '')
    if len(short) > MAX_SHORT_LENGTH or not SHORT_PATTERN.fullmatch(short):
        raise InvalidAPIUsage(API_ERROR_INVALID_SHORT, HTTPStatus.BAD_REQUEST)
    try:
        url_map = URLMap.create(original, short)
    except IntegrityError:
        raise InvalidAPIUsage(MESSAGE_SHORT_TAKEN)
    except RuntimeError as e:
        raise InvalidAPIUsage(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short>/', methods=['GET'])
def get_original(short):
    try:
        return (
            jsonify({'url': URLMap.get_url_map_by_short(short).original}),
            HTTPStatus.OK
        )
    except AttributeError:
        raise InvalidAPIUsage(API_ERROR_ID_NOT_FOUND, HTTPStatus.NOT_FOUND)

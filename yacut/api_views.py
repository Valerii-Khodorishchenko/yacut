import re
from flask import jsonify, request

from . import app, db
from .constants import MAX_SHORT_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


CUSTOM_ID_PATTERN = re.compile(rf'^[a-zA-Z0-9]{{0,{MAX_SHORT_LENGTH}}}$')


def validate_request_data(data):
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if (original := data.get('url')) is None:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if not (short := data.get('custom_id', '')):
        try:
            short = get_unique_short_id()
        except RuntimeError as e:
            raise InvalidAPIUsage(str(e), 500)
    elif not CUSTOM_ID_PATTERN.fullmatch(short):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    return original, short


@app.route('/api/id/', methods=['POST'])
def create_id():
    original, short = validate_request_data(request.get_json(silent=True))
    if URLMap.query.filter_by(short=short).first():
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    adapted_data = {
        'original': original,
        'short': short
    }
    url_map = URLMap(**adapted_data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200

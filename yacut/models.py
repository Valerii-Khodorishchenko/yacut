import random
from datetime import datetime, timezone

from flask import url_for
from validators import url as validate_url

from yacut import db
from .constants import (
    ATTEMPTS_TO_GENERATE,
    CHARSET,
    ERROR_INVALID_ORIGINAL,
    ERROR_INVALID_SHORT,
    ERROR_SHORT_TAKEN,
    GET_SHORT_ENDPOINT,
    LENGTH_GENERATED_SHORT,
    MAX_ORIGINAL_LENGTH,
    MAX_SHORT_LENGTH,
    SHORT_PATTERN
)


ERROR_UNIQUE_SHORT_FAIL = 'Не удалось сгенерировать короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.get_short_link()
        }

    def get_short_link(self):
        return url_for(GET_SHORT_ENDPOINT, short=self.short, _external=True)

    @staticmethod
    def create(original, short=None):
        URLMap.validate_original(original)
        if short == '' or short is None:
            short = URLMap.generate_unique_short()
        else:
            URLMap.validate_short(short)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def validate_original(original):
        if len(original) > MAX_ORIGINAL_LENGTH or not validate_url(original):
            raise ValueError(ERROR_INVALID_ORIGINAL)

    @staticmethod
    def validate_short(short):
        if len(short) > MAX_SHORT_LENGTH or not SHORT_PATTERN.fullmatch(short):
            raise ValueError(ERROR_INVALID_SHORT)
        elif URLMap.get_or_false(short):
            raise ValueError(ERROR_SHORT_TAKEN)

    @staticmethod
    def generate_unique_short():
        for _ in range(ATTEMPTS_TO_GENERATE):
            short = ''.join(random.choices(
                CHARSET, k=LENGTH_GENERATED_SHORT
            ))
            if not URLMap.get_or_false(short):
                return short
        raise RuntimeError(ERROR_UNIQUE_SHORT_FAIL)

    @staticmethod
    def get_or_false(short=None):
        url_map = URLMap.query.filter_by(short=short).first()
        return False if url_map is None else url_map

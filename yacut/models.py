import random
from datetime import datetime, timezone

from flask import request

from yacut import db
from .constants import CHARSET, MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH


ATTEMPTS_TO_GENERATE = 10
LENGTH_GENERATED_SHORT = 6
NOT_GET_UNIQUE_SHORT_ID = 'Не удалось сгенерировать короткую ссылку.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )

    @classmethod
    def create(cls, original, short):
        if short == '' or short is None:
            for _ in range(ATTEMPTS_TO_GENERATE):
                short = ''.join(random.choices(
                    CHARSET, k=LENGTH_GENERATED_SHORT
                ))
                if not cls.is_short_taken(short):
                    break
            else:
                raise RuntimeError(NOT_GET_UNIQUE_SHORT_ID)
        url_map = cls(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': self.get_short_link(self.short)
        }

    @staticmethod
    def is_short_taken(short):
        return URLMap.get_url_map_by_short(short) is not None

    @staticmethod
    def get_url_map_by_short(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_short_link(short):
        return request.host_url.rstrip('/') + '/{}'.format(short)

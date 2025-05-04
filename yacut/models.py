import random
from datetime import datetime, timezone

from flask import url_for

from yacut import db
from .constants import (
    ATTEMPTS_TO_GENERATE,
    CHARSET,
    LENGTH_GENERATED_SHORT,
    MAX_ORIGINAL_LENGTH,
    MAX_SHORT_LENGTH,
    SHORT_PATTERN
)


ERROR_UNIQUE_SHORT_FAIL = 'Не удалось сгенерировать короткую ссылку'
ERROR_INVALID_ORIGINAL = 'Указано недопустимое имя ссылки'
ERROR_INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
ERROR_SHORT_TAKEN = 'Предложенный вариант короткой ссылки уже существует.'

REDIRECT_FUNCTION = 'redirect_to_original'


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
        return url_for(REDIRECT_FUNCTION, short=self.short, _external=True)

    @staticmethod
    def create(original, short=None, do_validate=True):
        if do_validate and len(original) > MAX_ORIGINAL_LENGTH:
            raise ValueError(ERROR_INVALID_ORIGINAL)
        if not short:
            short = URLMap.generate_unique_short()
        elif do_validate:
            if (
                len(short) > MAX_SHORT_LENGTH
                or not SHORT_PATTERN.fullmatch(short)
            ):
                raise ValueError(ERROR_INVALID_SHORT)
            if URLMap.get(short):
                raise ValueError(ERROR_SHORT_TAKEN)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def generate_unique_short():
        for _ in range(ATTEMPTS_TO_GENERATE):
            short = ''.join(random.choices(
                CHARSET, k=LENGTH_GENERATED_SHORT
            ))
            if not URLMap.get(short):
                return short
        raise RuntimeError(ERROR_UNIQUE_SHORT_FAIL)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

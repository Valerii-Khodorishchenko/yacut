from datetime import datetime, timezone

from flask import url_for

from yacut import db
from .constants import MAX_SHORT_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(2048), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), nullable=False, unique=True)
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            'url': self.original,
            'short_link': url_for(
                'redirect_to_original',
                short=self.short,
                _external=True
            )
        }

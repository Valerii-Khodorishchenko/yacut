from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    URL,
    ValidationError
)

from .models import URLMap
from .constants import MAX_SHORT_LENGTH


class UniqueURL:
    def __call__(self, form, field):
        if not field.data:
            return
        if URLMap.query.filter_by(short=field.data).first() is not None:
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(
            DataRequired(message='Обязательное поле'),
            Length(1, 2048, message='Это много даже для меня.'),
            URL(message='Похоже, это не ссылка! Пожалуйста, проверьте адрес.')
        )
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Optional(),
            Length(1, MAX_SHORT_LENGTH, message='Не длиннее 16 символов'),
            UniqueURL()
        )
    )
    submit = SubmitField('Создать')

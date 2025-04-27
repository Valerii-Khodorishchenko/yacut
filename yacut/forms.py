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


class UniqueURL:
    def __call__(self, form, field):
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
            Length(1, 16, message='Не длиннее 16 символов'),
            Optional(),
            UniqueURL()
        )
    )
    submit = SubmitField('Создать')

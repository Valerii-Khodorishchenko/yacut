from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    URL,
    ValidationError
)

from .constants import (
    MAX_ORIGINAL_LENGTH,
    MAX_SHORT_LENGTH,
    MESSAGE_SHORT_TAKEN
)
from .models import URLMap


MESSAGE_REQUIRED = 'Обязательное поле'
MESSAGE_TOO_LONG = 'Не длиннее {} символов'
MESSAGE_NOT_URL = 'Похоже, это не ссылка! Пожалуйста, проверьте адрес.'
ORIGINAL_LINK_DESCRIPTION = 'Длинная ссылка'
CUSTOM_ID_DESCRIPTION = 'Ваш вариант короткой ссылки'
SUBMIT = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_DESCRIPTION,
        validators=(
            DataRequired(message=MESSAGE_REQUIRED),
            Length(
                max=MAX_ORIGINAL_LENGTH,
                message=MESSAGE_TOO_LONG.format(MAX_ORIGINAL_LENGTH)
            ),
            URL(message=MESSAGE_NOT_URL)
        )
    )
    custom_id = StringField(
        CUSTOM_ID_DESCRIPTION,
        validators=(
            Optional(),
            Length(
                max=MAX_SHORT_LENGTH,
                message=MESSAGE_TOO_LONG.format(MAX_SHORT_LENGTH)
            )
        )
    )
    submit = SubmitField(SUBMIT)

    def validate_custom_id(self, field):
        if field.data.strip() and URLMap.is_short_taken(field.data):
            raise ValidationError(MESSAGE_SHORT_TAKEN)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    URL,
    ValidationError
)

from .constants import (

    MAX_ORIGINAL_LENGTH,
    MAX_SHORT_LENGTH,
    SHORT_PATTERN
)
from .models import (
    URLMap,
    ERROR_INVALID_ORIGINAL,
    ERROR_INVALID_SHORT,
    ERROR_SHORT_TAKEN,
)

MESSAGE_REQUIRED = 'Обязательное поле'
MESSAGE_TOO_LONG = 'Не длиннее {} символов'
MESSAGE_TOO_LONG_ORIGINAL = MESSAGE_TOO_LONG.format(MAX_ORIGINAL_LENGTH)
MESSAGE_TOO_LONG_SHORT = MESSAGE_TOO_LONG.format(MAX_SHORT_LENGTH)

ORIGINAL_LINK_DESCRIPTION = 'Длинная ссылка'
SHORT_DESCRIPTION = 'Ваш вариант короткой ссылки'
SUBMIT = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LINK_DESCRIPTION,
        validators=(
            DataRequired(message=MESSAGE_REQUIRED),
            Length(
                max=MAX_ORIGINAL_LENGTH,
                message=MESSAGE_TOO_LONG_ORIGINAL
            ),
            URL(message=ERROR_INVALID_ORIGINAL)
        )
    )
    custom_id = StringField(
        SHORT_DESCRIPTION,
        validators=(
            Optional(),
            Length(
                max=MAX_SHORT_LENGTH,
                message=MESSAGE_TOO_LONG_SHORT
            ),
            Regexp(
                SHORT_PATTERN,
                message=ERROR_INVALID_SHORT
            )
        )
    )
    submit = SubmitField(SUBMIT)

    def validate_custom_id(self, field):
        if field.data.strip() and URLMap.get(field.data):
            raise ValidationError(ERROR_SHORT_TAKEN)

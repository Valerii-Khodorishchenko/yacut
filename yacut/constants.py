import re
import string

from . import app

GET_SHORT_ENDPOINT = app.config['DOMAIN_NAME']

MAX_SHORT_LENGTH = 16
MAX_ORIGINAL_LENGTH = 2048

ATTEMPTS_TO_GENERATE = 10
LENGTH_GENERATED_SHORT = 6
CHARSET = string.ascii_letters + string.digits
SHORT_PATTERN = re.compile(rf'^[{CHARSET}]*$')

ERROR_INVALID_ORIGINAL = 'Указано недопустимое имя ссылки'
ERROR_INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
ERROR_SHORT_TAKEN = 'Предложенный вариант короткой ссылки уже существует.'

import re
import string


MAX_SHORT_LENGTH = 16
MAX_ORIGINAL_LENGTH = 2048

ATTEMPTS_TO_GENERATE = 10
LENGTH_GENERATED_SHORT = 6
CHARSET = string.ascii_letters + string.digits
SHORT_PATTERN = re.compile(rf'^[{CHARSET}]*$')

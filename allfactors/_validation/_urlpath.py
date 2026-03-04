import re

from allfactors._errors import ValidationError
from allfactors._validation._limits import LIMITS

_VALID_PATH_RE = re.compile(r"^/[a-zA-Z0-9\-._~!$&'()*+,;=:@/]*$")


def validate_path(value: object) -> str:
    if not isinstance(value, str):
        raise ValidationError('path must be a string', 'path')
    if not _VALID_PATH_RE.match(value):
        raise ValidationError("path must be a valid URL path starting with '/'", 'path')
    if len(value) > LIMITS['PATH_MAX_LENGTH']:
        raise ValidationError(f'path: Max length is {LIMITS["PATH_MAX_LENGTH"]} characters', 'path')
    return value

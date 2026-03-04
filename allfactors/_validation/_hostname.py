import re

from allfactors._errors import ValidationError
from allfactors._validation._limits import LIMITS
from allfactors._validation._sanitize import sanitize_string

_HOSTNAME_RE = re.compile(r'^[a-zA-Z0-9.-]+$')


def validate_hostname(value: object, field: str = 'hostname') -> str:
    if not isinstance(value, str):
        raise ValidationError(f'{field} must be a string', field)

    sanitized = sanitize_string(
        value,
        trim=True,
        normalize_unicode=True,
        reject_control_chars=True,
        normalize_whitespace=True,
        to_lower_case=True,
    )

    if len(sanitized) == 0:
        raise ValidationError(f'{field} must be a non-empty string', field)
    if len(sanitized) > LIMITS['HOSTNAME_MAX_LENGTH']:
        raise ValidationError(f'{field}: Max length is {LIMITS["HOSTNAME_MAX_LENGTH"]} characters', field)
    if not _HOSTNAME_RE.match(sanitized):
        raise ValidationError(f'{field}: Invalid format', field)

    return sanitized

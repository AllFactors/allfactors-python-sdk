import re

from allfactors._errors import ValidationError
from allfactors._validation._limits import LIMITS
from allfactors._validation._sanitize import sanitize_string

_EMAIL_RE = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')


def validate_email(value: object, field: str = 'email') -> str:
    if not isinstance(value, str):
        raise ValidationError(f'{field} must be a string', field)

    sanitized = sanitize_string(
        value,
        trim=True,
        normalize_unicode=True,
        reject_control_chars=True,
        normalize_whitespace=True,
        to_lower_case=False,
    )

    at_index = sanitized.rfind('@')
    if at_index > 0:
        local = sanitized[:at_index]
        domain = sanitized[at_index + 1:].lower()
        sanitized = local + '@' + domain

    if not (LIMITS['EMAIL_MIN_LENGTH'] <= len(sanitized) <= LIMITS['EMAIL_MAX_LENGTH']):
        raise ValidationError(
            f'{field}: Length must be between {LIMITS["EMAIL_MIN_LENGTH"]} and {LIMITS["EMAIL_MAX_LENGTH"]}',
            field,
        )

    if not _EMAIL_RE.match(sanitized):
        raise ValidationError(f'{field}: Invalid format', field)

    return sanitized

from allfactors._errors import ValidationError
from allfactors._validation._sanitize import sanitize_string


def validate_string(
    value: object,
    *,
    field: str,
    max_length: int | None = None,
    min_length: int = 0,
    allow_empty: bool = False,
    secret: bool = False,
) -> str:
    if not isinstance(value, str):
        raise ValidationError(f'{field} must be a string', field)

    sanitized = sanitize_string(
        value,
        trim=True,
        normalize_unicode=True,
        reject_control_chars=True,
        normalize_whitespace=not secret,
        to_lower_case=False,
        is_secret=secret,
    )

    length = len(sanitized)
    if not allow_empty and length == 0:
        raise ValidationError(f'{field} must be a non-empty string', field)
    if length < min_length:
        raise ValidationError(f'{field}: Min length is {min_length} characters', field)
    if max_length is not None and length > max_length:
        raise ValidationError(f'{field}: Max length is {max_length} characters', field)

    return sanitized

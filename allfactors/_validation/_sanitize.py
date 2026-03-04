import re
import unicodedata

from allfactors._errors import ValidationError

_CONTROL_CHAR_RE = re.compile(r'[\x00-\x1F\x7F-\x9F]')
_UNICODE_WHITESPACE_RE = re.compile(r'[\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000]')
_MULTI_WHITESPACE_RE = re.compile(r'\s+')


def sanitize_string(
    value: str,
    *,
    trim: bool = True,
    normalize_unicode: bool = True,
    reject_control_chars: bool = True,
    normalize_whitespace: bool = True,
    to_lower_case: bool = False,
    is_secret: bool = False,
) -> str:
    result = value

    if trim:
        result = result.strip()

    if normalize_unicode:
        result = unicodedata.normalize('NFC', result)

    if reject_control_chars:
        if _CONTROL_CHAR_RE.search(result):
            raise ValidationError('Input contains invalid control characters', 'sanitize')

    if normalize_whitespace and not is_secret:
        result = _UNICODE_WHITESPACE_RE.sub(' ', result)
        result = _MULTI_WHITESPACE_RE.sub(' ', result)

    if to_lower_case:
        result = result.lower()

    return result

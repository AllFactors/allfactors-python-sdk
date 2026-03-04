from dataclasses import dataclass

from allfactors._errors import ValidationError
from allfactors._validation._email import validate_email
from allfactors._validation._hostname import validate_hostname
from allfactors._validation._limits import LIMITS
from allfactors._validation._strings import validate_string
from allfactors._validation._urlpath import validate_path

_VALID_TYPES = frozenset({'oauth', 'form'})


def _validate_type(value: object) -> str:
    if not isinstance(value, str) or value not in _VALID_TYPES:
        raise ValidationError("type must be 'oauth' or 'form'", 'type')
    return value


@dataclass
class SanitizedSignupArgs:
    email: str
    type: str
    hostname: str
    path: str
    af_usr: str
    af_ses: str


def validate_signup_args(
    email: object,
    type: object,
    hostname: object,
    path: object,
    af_usr: object,
    af_ses: object,
) -> SanitizedSignupArgs:
    return SanitizedSignupArgs(
        email=validate_email(email, 'email'),
        type=_validate_type(type),
        hostname=validate_hostname(hostname, 'hostname'),
        path=validate_path(path),
        af_usr=validate_string(
            af_usr,
            field='af_usr',
            allow_empty=False,
            min_length=LIMITS['AF_USR_LENGTH'],
            max_length=LIMITS['AF_USR_LENGTH'],
        ),
        af_ses=validate_string(
            af_ses,
            field='af_ses',
            allow_empty=False,
            min_length=LIMITS['AF_SES_LENGTH'],
            max_length=LIMITS['AF_SES_LENGTH'],
        ),
    )

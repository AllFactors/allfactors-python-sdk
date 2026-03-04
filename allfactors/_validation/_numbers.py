from allfactors._errors import ValidationError
from allfactors._validation._limits import LIMITS


def validate_port(value: object, field: str = 'port') -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(f'{field} must be an integer', field)
    if not (LIMITS['PORT_MIN'] <= value <= LIMITS['PORT_MAX']):
        raise ValidationError(
            f'{field} must be a number between {LIMITS["PORT_MIN"]} and {LIMITS["PORT_MAX"]}',
            field,
        )

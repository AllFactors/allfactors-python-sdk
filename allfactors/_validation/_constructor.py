from dataclasses import dataclass, field

from allfactors._errors import ValidationError
from allfactors._validation._limits import LIMITS
from allfactors._validation._numbers import validate_port
from allfactors._validation._strings import validate_string

_ALLOWED_PROTOCOLS = frozenset({'http', 'https'})


@dataclass
class ProxyAuth:
    username: str
    password: str


@dataclass
class SanitizedProxyConfig:
    host: str
    port: int
    protocol: str | None = None
    auth: ProxyAuth | None = None


@dataclass
class SanitizedConstructorArgs:
    domain: str
    access_key: str
    secret_key: str
    proxy: SanitizedProxyConfig | None = None


def validate_constructor_args(
    domain: object,
    access_key: object,
    secret_key: object,
    config: object = None,
) -> SanitizedConstructorArgs:
    sanitized_domain = validate_string(
        domain, field='domain', allow_empty=False, max_length=LIMITS['DOMAIN_MAX_LENGTH']
    )
    sanitized_access_key = validate_string(
        access_key, field='accessKey', allow_empty=False, max_length=LIMITS['ACCESS_KEY_MAX_LENGTH'], secret=True
    )
    sanitized_secret_key = validate_string(
        secret_key, field='secretKey', allow_empty=False, max_length=LIMITS['SECRET_KEY_MAX_LENGTH'], secret=True
    )

    if config is None:
        return SanitizedConstructorArgs(
            domain=sanitized_domain,
            access_key=sanitized_access_key,
            secret_key=sanitized_secret_key,
        )

    if not isinstance(config, dict):
        raise ValidationError('config must be a dict', 'config')

    proxy = config.get('proxy')
    if not proxy:
        return SanitizedConstructorArgs(
            domain=sanitized_domain,
            access_key=sanitized_access_key,
            secret_key=sanitized_secret_key,
        )

    if not isinstance(proxy, dict):
        raise ValidationError('config.proxy must be a dict', 'config.proxy')

    sanitized_host = validate_string(
        proxy.get('host'), field='proxy.host', allow_empty=False, max_length=LIMITS['PROXY_HOST_MAX_LENGTH']
    )
    validate_port(proxy.get('port'), 'proxy.port')

    sanitized_protocol: str | None = None
    if proxy.get('protocol') is not None:
        if not isinstance(proxy['protocol'], str):
            raise ValidationError('proxy.protocol must be a string', 'proxy.protocol')
        p = proxy['protocol'].lower()
        if p not in _ALLOWED_PROTOCOLS:
            raise ValidationError('proxy.protocol must be one of: http, https', 'proxy.protocol')
        sanitized_protocol = p

    sanitized_auth: ProxyAuth | None = None
    if proxy.get('auth'):
        auth = proxy['auth']
        sanitized_auth = ProxyAuth(
            username=validate_string(
                auth.get('username'),
                field='proxy.auth.username',
                allow_empty=False,
                max_length=LIMITS['PROXY_AUTH_STRING_MAX_LENGTH'],
                secret=True,
            ),
            password=validate_string(
                auth.get('password'),
                field='proxy.auth.password',
                allow_empty=False,
                max_length=LIMITS['PROXY_AUTH_STRING_MAX_LENGTH'],
                secret=True,
            ),
        )

    return SanitizedConstructorArgs(
        domain=sanitized_domain,
        access_key=sanitized_access_key,
        secret_key=sanitized_secret_key,
        proxy=SanitizedProxyConfig(
            host=sanitized_host,
            port=proxy['port'],
            protocol=sanitized_protocol,
            auth=sanitized_auth,
        ),
    )

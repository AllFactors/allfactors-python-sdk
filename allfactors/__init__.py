from allfactors._client import AllFactors, AsyncAllFactors
from allfactors._errors import ValidationError

__all__ = [
    'AllFactors', 'AsyncAllFactors', 'ValidationError',
    'init', 'async_init',
    'validate', 'send_signup',
    'async_validate', 'async_send_signup',
]

_client: AllFactors | None = None
_async_client: AsyncAllFactors | None = None


def init(
    domain: str,
    access_key: str,
    secret_key: str,
    config: dict | None = None,
) -> None:
    """Initialize the global sync client. Call once at startup."""
    global _client
    _client = AllFactors(domain, access_key, secret_key, config)


def async_init(
    domain: str,
    access_key: str,
    secret_key: str,
    config: dict | None = None,
) -> None:
    """Initialize the global async client. Call once at startup."""
    global _async_client
    _async_client = AsyncAllFactors(domain, access_key, secret_key, config)


def _require_client() -> AllFactors:
    if _client is None:
        raise RuntimeError("AllFactors not initialized. Call allfactors.init() first.")
    return _client


def _require_async_client() -> AsyncAllFactors:
    if _async_client is None:
        raise RuntimeError("AllFactors not initialized. Call allfactors.async_init() first.")
    return _async_client


def validate() -> dict:
    return _require_client().validate()


def send_signup(
    email: str,
    type: str,
    hostname: str,
    path: str,
    af_usr: str,
    af_ses: str,
) -> dict:
    return _require_client().send_signup(email, type, hostname, path, af_usr, af_ses)


async def async_validate() -> dict:
    return await _require_async_client().validate()


async def async_send_signup(
    email: str,
    type: str,
    hostname: str,
    path: str,
    af_usr: str,
    af_ses: str,
) -> dict:
    return await _require_async_client().send_signup(email, type, hostname, path, af_usr, af_ses)

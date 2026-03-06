import hashlib
import hmac
import json
import time
from importlib.metadata import version, PackageNotFoundError
import httpx

from allfactors._validation._constructor import validate_constructor_args, SanitizedProxyConfig
from allfactors._validation._signup import validate_signup_args

try:
    VERSION = version('allfactors')
except PackageNotFoundError:
    VERSION = '1.0.2' # fallback version if package metadata is not available

_BASE_URL = 'https://sdk-events.allfactors.com'
_TIMEOUT = 30.0
_USER_AGENT = f'allfactors-python-sdk/{VERSION}'


def _build_proxy_url(proxy: SanitizedProxyConfig) -> str:
    protocol = proxy.protocol or 'http'
    if proxy.auth:
        return f'{protocol}://{proxy.auth.username}:{proxy.auth.password}@{proxy.host}:{proxy.port}'
    return f'{protocol}://{proxy.host}:{proxy.port}'


def _hmac_signature(secret_key: str, data: dict) -> str:
    message = json.dumps(data, separators=(',', ':'))
    return hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).hexdigest()


def _extract_error(response: httpx.Response) -> str:
    try:
        body = response.json()
        if isinstance(body, dict) and 'error' in body:
            return str(body['error'])
    except Exception:
        pass
    return f'{response.status_code} - {response.reason_phrase}'


class AllFactors:
    """Synchronous AllFactors SDK client"""

    def __init__(
        self,
        domain: str,
        access_key: str,
        secret_key: str,
        config: dict | None = None,
    ) -> None:
        args = validate_constructor_args(domain, access_key, secret_key, config)
        self._domain = args.domain
        self._access_key = args.access_key
        self._secret_key = args.secret_key

        proxy_url = _build_proxy_url(args.proxy) if args.proxy else None
        self._client = httpx.Client(
            base_url=_BASE_URL,
            headers={'User-Agent': _USER_AGENT},
            timeout=_TIMEOUT,
            proxy=proxy_url,
        )

    def validate(self) -> dict:
        ts = int(time.time() * 1000)
        payload = {'access_key': self._access_key, 'ts': ts}
        signature = _hmac_signature(self._secret_key, payload)

        try:
            response = self._client.post(
                f'/api/v1/validate/{self._domain}/',
                json=payload,
                headers={'X-Signature': signature, 'X-Access-Key': self._access_key},
            )
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or data.get('status') != 'ok':
                raise Exception('AllFactors validation failed: unexpected response from server')
            return data
        except httpx.HTTPStatusError as exc:
            raise Exception(f'AllFactors validation failed: {_extract_error(exc.response)}') from exc

    def send_signup(
        self,
        email: str,
        type: str,
        hostname: str,
        path: str,
        af_usr: str,
        af_ses: str,
    ) -> dict:
        sanitized = validate_signup_args(email, type, hostname, path, af_usr, af_ses)
        ts = int(time.time() * 1000)
        payload = {
            'type': sanitized.type,
            'email': sanitized.email,
            'hostname': sanitized.hostname,
            'path': sanitized.path,
            'af_usr': sanitized.af_usr,
            'af_ses': sanitized.af_ses,
            'ts': ts,
            'access_key': self._access_key,
        }
        signature = _hmac_signature(self._secret_key, payload)

        try:
            response = self._client.post(
                f'/api/v1/signup/{self._domain}/',
                json=payload,
                headers={'X-Signature': signature, 'X-Access-Key': self._access_key},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise Exception(f'AllFactors API Error: {_extract_error(exc.response)}') from exc

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> 'AllFactors':
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncAllFactors:
    """Asynchronous AllFactors SDK client"""

    def __init__(
        self,
        domain: str,
        access_key: str,
        secret_key: str,
        config: dict | None = None,
    ) -> None:
        args = validate_constructor_args(domain, access_key, secret_key, config)
        self._domain = args.domain
        self._access_key = args.access_key
        self._secret_key = args.secret_key

        proxy_url = _build_proxy_url(args.proxy) if args.proxy else None
        self._client = httpx.AsyncClient(
            base_url=_BASE_URL,
            headers={'User-Agent': _USER_AGENT},
            timeout=_TIMEOUT,
            proxy=proxy_url,
        )

    async def validate(self) -> dict:
        ts = int(time.time() * 1000)
        payload = {'access_key': self._access_key, 'ts': ts}
        signature = _hmac_signature(self._secret_key, payload)

        try:
            response = await self._client.post(
                f'/api/v1/validate/{self._domain}/',
                json=payload,
                headers={'X-Signature': signature, 'X-Access-Key': self._access_key},
            )
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, dict) or data.get('status') != 'ok':
                raise Exception('AllFactors validation failed: unexpected response from server')
            return data
        except httpx.HTTPStatusError as exc:
            raise Exception(f'AllFactors validation failed: {_extract_error(exc.response)}') from exc

    async def send_signup(
        self,
        email: str,
        type: str,
        hostname: str,
        path: str,
        af_usr: str,
        af_ses: str,
    ) -> dict:
        sanitized = validate_signup_args(email, type, hostname, path, af_usr, af_ses)
        ts = int(time.time() * 1000)
        payload = {
            'type': sanitized.type,
            'email': sanitized.email,
            'hostname': sanitized.hostname,
            'path': sanitized.path,
            'af_usr': sanitized.af_usr,
            'af_ses': sanitized.af_ses,
            'ts': ts,
            'access_key': self._access_key,
        }
        signature = _hmac_signature(self._secret_key, payload)

        try:
            response = await self._client.post(
                f'/api/v1/signup/{self._domain}/',
                json=payload,
                headers={'X-Signature': signature, 'X-Access-Key': self._access_key},
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise Exception(f'AllFactors API Error: {_extract_error(exc.response)}') from exc

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> 'AsyncAllFactors':
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

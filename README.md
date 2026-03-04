# allfactors

Python server-side SDK for AllFactors Analytics

## Installation

```bash
pip install allfactors
```

or

```bash
uv add allfactors
```

## Usage

### Sync

```python
from allfactors import AllFactors

# Initialize the SDK
af = AllFactors('your-domain', 'your-access-key', 'your-secret-key')

# Helper to read cookies (implementation varies by framework)
# FastAPI: request.cookies.get(name)
# Django:  request.COOKIES.get(name)
# Flask:   request.cookies.get(name)
# Sanic:   request.cookies.get(name)

# Send a signup event
try:
    result = af.send_signup(
        'user@example.com',
        'form',
        'app.yourcompany.com',
        '/registration/signup',
        request.cookies.get('af_usr'),
        request.cookies.get('af_ses')
    )
    print('Signup tracked successfully:', result)
except Exception as e:
    print('Error tracking signup:', e)
```

### Async

```python
from allfactors import AsyncAllFactors
import logging

# Initialize the SDK
af = AsyncAllFactors('your-domain', 'your-access-key', 'your-secret-key')
logger = logging.getLogger(__name__)

# Helper to read cookies (implementation varies by framework)
# FastAPI: request.cookies.get(name)
# Django:  request.COOKIES.get(name)
# Flask:   request.cookies.get(name)
# Sanic:   request.cookies.get(name)

# Send a signup event
async def user_signup(request):
    email = request.body.get('email')
    af_usr = request.cookies.get('af_usr')
    af_ses = request.cookies.get('af_ses')

    if af_usr and af_ses:
        try:
            result = await af.send_signup(
                email,
                'form',
                'app.yourcompany.com',
                request.url.path,
                af_usr,
                af_ses
            )
            logger.info('Signup tracked successfully:', result)
        except Exception as e:
            logger.error('Error tracking signup:', e)

    # the rest of your user sign-up code
    return JSONResponse({'success': True}, status_code=201)
```

### With Proxy Configuration

```python
from allfactors import AllFactors

af = AllFactors('your-domain', 'your-access-key', 'your-secret-key', {
    'proxy': {
        'host': 'proxy.example.com',
        'port': 8080,
        'protocol': 'http',
        'auth': {
            'username': 'proxy-user',
            'password': 'proxy-password'
        }
    }
})

# Use the SDK as normal
af.send_signup('user@example.com',
               'form',
               'app.example.com',
               '/path/of/user/signup/page',
               request.cookies.get('af_usr'),
               request.cookies.get('af_ses')
               )
```

## API

### Constructor

```python
AllFactors(domain: str, access_key: str, secret_key: str, config: dict | None = None)
AsyncAllFactors(domain: str, access_key: str, secret_key: str, config: dict | None = None)
```

**Parameters:**
- `domain` (str): Your AllFactors domain
- `access_key` (str): Your AllFactors access key
- `secret_key` (str): Your AllFactors secret key
- `config` (optional dict): Configuration options
  - `proxy` (optional dict): Proxy server configuration
    - `host` (str): Proxy server hostname
    - `port` (int): Proxy server port
    - `protocol` (optional str): Proxy protocol (`'http'` or `'https'`)
    - `auth` (optional dict): Proxy authentication
      - `username` (str): Proxy username
      - `password` (str): Proxy password

### Methods

#### send_signup(email, type, hostname, path, af_usr, af_ses)

Sends a signup event to AllFactors.

**Parameters:**
- `email` (str): User email address
- `type` (str): Signup type - either `'oauth'` or `'form'`
- `hostname` (str): The hostname that the signup occured on
- `path` (str): The path of the page that the signup occured on
- `af_usr` (str): AllFactors user identifier (read from the `af_usr` HTTP cookie)
- `af_ses` (str): AllFactors session identifier (read from the `af_ses` HTTP cookie)

**Important:** The `af_usr` and `af_ses` parameters should be read from HTTP cookies set by the AllFactors client-side tracking script. Do not generate random values for these parameters.

**Returns:** `dict` with the API response

## Development

### Building

```bash
uv build
```

## License

MIT

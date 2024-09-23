# auth/auth.py
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests

AUTH0_DOMAIN = 'dev-4o8fj5mv3s5rdudi.us.auth0.com'
API_IDENTIFIER = 'https://your-api-endpoint/'
ALGORITHMS = ['RS256']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_jwks():
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    response = requests.get(jwks_url)
    return response.json()


def verify_jwt(token: str):
    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}

        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }

        if rsa_key:
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_IDENTIFIER)
            return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Could not validate credentials: {e}"
        )
    raise HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_jwt(token)
    print(f"Roles y permisos: {payload}")
    # Extrct roles of claims
    roles = payload.get('https://myapp.com/roles', [])
    print(f"Roles: {roles}")

    return {"user": payload, "roles": roles}

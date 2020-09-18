from os import environ
import json
from flask import Flask, request, jsonify, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTHO_DOMAIN = 'xiaojun.eu.auth0.com'  ###needs modification
ALGORITHMS = ['RS256']
API_AUDIENCE = 'pitchbooking'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''

token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Inh0RTIwbm1FQWtuZnNTQ1l2NVpRQiJ9.eyJpc3MiOiJodHRwczovL3hpYW9qdW4uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNGQwMzY1NTkzNTgwMDA2NzU0YTM1YyIsImF1ZCI6InBpdGNoYm9va2luZyIsImlhdCI6MTYwMDM1NDUxOCwiZXhwIjoxNjAwNDI2NTE4LCJhenAiOiJzT0hZSTZwYTBUZG11MWVYTnpxOVliNkNTUkhRcHUxcyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBpdGNoIiwiZ2V0OnBpdGNoIiwicGF0Y2g6cGl0Y2giLCJwb3N0OmJvb2tpbmciLCJwb3N0OnBpdGNoZXMiXX0.VOk621L1kS6cmgh_M-c0WbULJ2Ryao34aQPQh8sJZIbAKP8a_4VNi-Q2B1qXCnNlM05Iv6O060NXha6rpbnZJF_xYfm9qh5rTGJ0a3vP_IgwuRqfgcPvFeQ2sMgwQ1r3gYvRbWftUbEu0_SmPshowys2_iXLzaWTN0WrO1ZLFcKSXVOUiUA6ws-1BrqhKdZ_U4YmQNp1LgBgK4thQ72h17WaYQLoOCXNtVZa0dHu_PNTBaE6llGL_oO1VtnPcMQDv5FGDe3wW-0xefADbXjJYUz9qu5Di4gEBKH9wkv7eQlQQTV6-gp_0adncksFydCq68l5EdFZLtN1V0J-FFvPzQ"
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def get_token_auth_header():
    auth_header=token
    #auth_header = request.headers.get("Authorization", None)

    if not auth_header:
        raise AuthError({'code': 'authorization_header_missing',
                         'description':'Authorization header is expected'}, 401)

    header_parts = auth_header.split(' ')

    if len(header_parts) != 2 or not header_parts:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be in the format'
            ' Bearer token'}, 401)

    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'}, 401)

    return header_parts[1]





'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the
    payload
    !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission
    string is not in the payload permissions array
    return true otherwise
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission Not found',
        }, 403)
    return True


'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def verify_decode_jwt(token):
    # Get public key from Auth0
    jsonurl = urlopen(f'https://xiaojun.eu.auth0.com/.well-known/jwks.json')
   
    jwks = json.loads(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # Auth0 token should have a key id
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            break

    # verify the token
    if rsa_key:
        try:
            # Validate the token using the rsa_key
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://xiaojun.eu.auth0.com/'
            )
            return payload

        except jwt.ExpiredSignatureError:

            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:

            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:

            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims
    and check the requested permission
    return the decorator which passes the decoded payload to the
    decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except:
                abort(401)
            return f(payload, *args, **kwargs)
            check_permissions(permission,payload)
        return wrapper
    return requires_auth_decorator
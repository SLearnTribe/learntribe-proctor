"""
Created on 19/01/23

Author Rahul Joshi

Function to deal with JWT exchanged with keycloak.
"""

import json
import os
from functools import wraps
from flask import request
from jose import jwt


ISSUER = os.getenv('ISSUER', 'http://www.smilebat.xyz/realms/master')
KEYCLOAK_PUBLIC_KEY = '-----BEGIN PUBLIC KEY-----\n' + \
                      os.getenv('KEYCLOAK_PUBLIC_KEY',
                                'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApGAGPe+55uUHGdx6T/qhq9wbi+1EjG7qmlm2uPX1KUKYXMCkthtV5pMwR3YvAcnN0I8zweAaSiLBj7sarunBFBYCd9OEfF7EAT3gssWGRRI9TrtHkHWnu6qjh4qE2UY6i0znvQ7Pp5iOyPa+u21aLsxc/lZiOPOt1DSy5vkOVS7rN4Rex484Cj9NeSmfh7P9wyv9v6tooDghzV/x7lt3mwMxNQjILHiNUv5/yAgYhBGX6kH/LRvtTwZ3LK2aWHTfdqh/OdQUqV0XjNEgZ0nmuNLBr3bb8vVKbxz55OZMl1yWNG4/0ZfjO7Di2miw6T+lAt9gXZyCxEoZNGoaP8/9XwIDAQAB') + \
                      '\n-----END PUBLIC KEY-----'


def jwt_verification(f):
    """
    Decorator for the JWT validation.

    Usage :\n
    @app.route("/", methods=["GET"])\n
    @jwt_verification\n
    def index(decoded_jwt):\n
    return json.dumps({"message": "JWT verified","sub": decoded_jwt['sub']})

    :param :

    :return: Decoded JWT
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if len(request.headers.get("Authorization"))==0:
            return json.dumps({"error": "Invalid JWT"}), 401  # Unauthorized
        jwt_token = request.headers.get("Authorization").split(" ")[1]

        try:
            decoded_jwt = jwt.decode(jwt_token, KEYCLOAK_PUBLIC_KEY,
                                     algorithms=["PS384", "ES384", "RS384", "HS256", "HS512", "ES256", "RS256", "HS384",
                                                 "ES512", "PS256", "PS512", "RS512"],
                                     issuer=ISSUER,
                                     audience='account')
        except jwt.ExpiredSignatureError:
            return json.dumps({"error": "JWT has expired"}), 419  # Authentication Timeout
        except jwt.JWTClaimsError as e:
            print("Exception ######### "+str(e))
            return json.dumps({"error": "JWT has invalid claims"}), 400  # Bad Request
        except jwt.JWTError:
            return json.dumps({"error": "Invalid JWT"}), 401  # Unauthorized
        except Exception as e:
            return json.dumps({"error": str(e)}), 500  # Internal Server Error
        # print("Inside## "+decoded_jwt['sub'])
        return f(keycloak_id=decoded_jwt['sub'], *args, **kwargs)

    return decorated_function

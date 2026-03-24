import jwt
import os
from datetime import datetime


class JwtToken:
    _private_key = None
    _public_key = None
    _keys_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "keys")

    @classmethod
    def _get_private_key(cls):
        if cls._private_key is None:
            path = os.path.join(cls._keys_dir, "private.pem")
            with open(path, "r") as f:
                cls._private_key = f.read()
        return cls._private_key

    @classmethod
    def _get_public_key(cls):
        if cls._public_key is None:
            path = os.path.join(cls._keys_dir, "public.pem")
            with open(path, "r") as f:
                cls._public_key = f.read()
        return cls._public_key

    @classmethod
    def generate_jwt(cls, user_id: str, iat: datetime):
        payload = {"sub": user_id, "iat": int(iat.timestamp())}
        token = jwt.encode(payload, cls._get_private_key(), algorithm="RS256")
        return token

    @classmethod
    def verify_token(cls, token: str):
        try:
            payload = jwt.decode(token, cls._get_public_key(), algorithms=["RS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

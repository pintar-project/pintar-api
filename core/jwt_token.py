import jwt
import os
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class JwtToken:
    _private_key = None
    _public_key = None
    _keys_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "keys")

    @classmethod
    def _ensure_keys_exist(cls):
        if not os.path.exists(cls._keys_dir):
            os.makedirs(cls._keys_dir)

        private_key_path = os.path.join(cls._keys_dir, "private.pem")
        public_key_path = os.path.join(cls._keys_dir, "public.pem")

        if not os.path.exists(private_key_path) or not os.path.exists(public_key_path):
            key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            with open(private_key_path, "wb") as f:
                f.write(key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))

            with open(public_key_path, "wb") as f:
                f.write(key.public_key().public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                ))

    @classmethod
    def _get_private_key(cls):
        if cls._private_key is None:
            cls._ensure_keys_exist()
            path = os.path.join(cls._keys_dir, "private.pem")
            with open(path, "r") as f:
                cls._private_key = f.read()
        return cls._private_key

    @classmethod
    def _get_public_key(cls):
        if cls._public_key is None:
            cls._ensure_keys_exist()
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

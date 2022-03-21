import hashlib
import base64
import jwt

from config import settings


def encode_password(pwd: str) -> str:
    base64_pwd = base64.b64encode(pwd.encode('utf-8'))
    encode_pwd = hashlib.md5(base64_pwd).hexdigest()
    return encode_pwd


def generate_token(payload: dict) -> str:
    return jwt.encode(payload, key=settings.OAUTH_SECRET_KEY, algorithm="HS256")


def parse_token(token: str) -> dict:
    try:
        return jwt.decode(token, key=settings.OAUTH_SECRET_KEY, algorithms="HS256")
    except Exception as e:
        print(str(e))
        return None

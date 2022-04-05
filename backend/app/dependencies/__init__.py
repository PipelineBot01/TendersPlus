from fastapi import Header, HTTPException
from sqlalchemy.orm import Session

from db.mysql import session
from utils.auth import parse_token

from config import Settings


def get_db() -> Session:
    db = session()
    try:
        yield db
    finally:
        db.close()


async def check_access_token(X_TOKEN: str = Header(None)) -> str:
    payload = parse_token(X_TOKEN)
    if payload and 'email' in payload:
        return payload['email']
    raise HTTPException(403, 'INVALID TOKEN')


async def check_admin_token(X_TOKEN: str = Header(None)) -> bool:
    if X_TOKEN != Settings.ADMIN_USER_TOKEN:
        raise HTTPException(403, 'INVALID TOKEN')
    return True

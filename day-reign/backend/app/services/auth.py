import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Request
from pwdlib import PasswordHash

from app.database import get_database

password_hash = PasswordHash.recommended()

SESSION_DAYS = 30
COOKIE_NAME = "dayreign_session"

def utc_now():
    return datetime.now(timezone.utc)

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

async def create_session(user_id: str) -> str:
    token = secrets.token_urlsafe(32)

    await get_database()["sessions"].insert_one({
        "tokenHash": hash_token(token),
        "userId": user_id,
        "expiresAt": utc_now() + timedelta(days=SESSION_DAYS)
    })

    return token


async def current_user(request: Request):
    token = request.cookies.get(COOKIE_NAME)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    db = get_database()

    session = await db["sessions"].find_one({
        "tokenHash": hash_token(token),
        "expiresAt": {"$gt": utc_now()}
    })

    if session is None:
        raise HTTPException(
            status_code = 401,
            detail = "Session expired or invalid"
        )

    user = await db["users"].find_one({
        "id": session["userId"]
    })

    if user is None:
        raise HTTPException(
            status_code=401,
            detail = "User Not Found"
        )

    # Renew an active session when it has
    # fewer than 15 days remaining.
    expiry = session["expiresAt"]

    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)
    remaining = expiry - utc_now()

    if remaining < timedelta(days=15):
        request.state.renew_session = token
    return user

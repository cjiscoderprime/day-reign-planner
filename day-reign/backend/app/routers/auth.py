from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pymongo.errors import DuplicateKeyError

from app.config import settings
from app.database import get_database
from app.models.user import RegisterInput, LoginInput, UserResponse
from app.services.auth import (
    COOKIE_NAME,
    SESSION_DAYS,
    create_session,
    current_user,
    hash_token,
    password_hash
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

def set_session_cookie(response: Response, token: str):
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=SESSION_DAYS * 24 * 60 * 60,
        path="/"
    )


def public_user(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
async def register(data: RegisterInput, response: Response):
    db = get_database()

    email = str(data.email).lower()

    document = {
        "id": str(uuid4()),
        "name": data.name.strip(),
        "email": email,
        "passwordHash": password_hash.hash(data.password)
    }

    if not document["name"]:
        raise HTTPException(422, "Name is required")

    try:
        await db["users"].insert_one(document)
    except DuplicateKeyError:
        raise HTTPException(409, "Email already registered")

    token = await create_session(document["id"])
    set_session_cookie(response, token)

    return public_user(document)


@router.post("/login", response_model=UserResponse)
async def login(data: LoginInput, response: Response):
    db = get_database()

    user = await db["users"].find_one({
        "email": str(data.email).lower()
    })

    if not user or not password_hash.verify(
        data.password,
        user["passwordHash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = await create_session(user["id"])
    set_session_cookie(response, token)

    return public_user(user)


@router.get("/me", response_model=UserResponse)
async def me(user=Depends(current_user)):
    return public_user(user)


@router.post("/logout")
async def logout(
    request: Request,
    response: Response
):
    token = request.cookies.get(COOKIE_NAME)

    if token:
        await get_database()["sessions"].delete_one({
            "tokenHash": hash_token(token)
        })

    response.delete_cookie(
        COOKIE_NAME,
        path="/",
        secure=settings.cookie_secure,
        samesite="lax"
    )

    return {"message": "Logged out"}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.routers.events import router as events_router
from app.config import settings
from app.database import check_database

from datetime import timedelta

from fastapi import Request
from fastapi.responses import JSONResponse

from contextlib import asynccontextmanager
from pymongo import ASCENDING

from app.database import get_database
from app.services.auth import (
    SESSION_DAYS,
    utc_now,
    hash_token
)
from app.routers.auth import (
    router as auth_router,
    set_session_cookie
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_database()

    await db["users"].create_index(
        [("email", ASCENDING)],
        unique=True
    )

    await db["sessions"].create_index(
        [("tokenHash", ASCENDING)],
        unique=True
    )

    await db["sessions"].create_index(
        [("expiresAt", ASCENDING)],
        expireAfterSeconds=0
    )

    yield

app = FastAPI(
    title = "DayReign API",
    description = "Backend for DayReign Personal Tracker",
    version = "0.2.0",
    lifespan=lifespan
)

app.include_router(events_router)

app.include_router(auth_router)

@app.middleware("http")
async def security_middleware(request: Request, call_next):
    # Require trusted browser origins for state-changing requests.
    if request.method in {"POST", "PATCH", "PUT", "DELETE"}:
        origin = request.headers.get("origin")

        if origin != settings.frontend_origin:
            return JSONResponse(
                {"detail": "Untrusted request origin"},
                status_code=403
            )

    response = await call_next(request)

    token = getattr(request.state, "renew_session", None)

    if token and response.status_code < 400:
        from datetime import timedelta

        await get_database()["sessions"].update_one(
            {"tokenHash": hash_token(token)},
            {"$set": {
                "expiresAt": utc_now() + timedelta(
                    days=SESSION_DAYS
                )
            }}
        )
        set_session_cookie(response, token)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials = True,
    allow_methods = ["GET", "POST", "PATCH", "DELETE"],
    allow_headers = ["Content-Type", "Authorization"]
)

@app.get("/")
async def home():
    return {
        "application": "DayReign API",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db")
async def database_health():
    try:
        await check_database()
        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=503,
            detail = "Database unavailable"
        )


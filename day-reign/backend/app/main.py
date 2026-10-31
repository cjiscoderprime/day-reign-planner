from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.routers.events import router as events_router
from app.config import settings
from app.database import check_database

app = FastAPI(
    title = "DayReignAPI",
    description = "Backend for DayReign Personal Tracker",
    version = "0.1.0"
)
app.include_router(events_router)

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
from pymongo import AsyncMongoClient

from app.config import settings

client = AsyncMongoClient(settings.mongodb_uri)

def get_database():
    return client[settings.mongodb_db]

async def check_database() -> bool:
    database = get_database()
    await database.command("ping")
    return True
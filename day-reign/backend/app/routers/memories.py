
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.database import get_database
from app.models.memory import MemoryInput, MemoryResponse
from app.services.auth import current_user


router = APIRouter(
    prefix="/api/memories",
    tags=["Memories"]
)


def collection():
    return get_database()["memories"]


@router.get("", response_model=list[MemoryResponse])
async def list_memories(user=Depends(current_user)):
    cursor = collection().find(
        {"userId": user["id"]},
        {"_id": 0, "userId": 0}
    ).sort([("date", -1), ("createdAt", -1)])

    return await cursor.to_list(length=1000)


@router.post(
    "",
    response_model=MemoryResponse,
    status_code=201
)
async def create_memory(
    memory: MemoryInput,
    user=Depends(current_user)
):
    now = datetime.now(timezone.utc).isoformat()

    document = {
        "id": str(uuid4()),
        "userId": user["id"],
        **memory.model_dump(),
        "createdAt": now,
        "updatedAt": now
    }

    await collection().insert_one(document)

    return document


@router.patch(
    "/{memory_id}",
    response_model=MemoryResponse
)
async def update_memory(
    memory_id: str,
    memory: MemoryInput,
    user=Depends(current_user)
):
    updates = {
        **memory.model_dump(),
        "updatedAt": datetime.now(
            timezone.utc
        ).isoformat()
    }

    result = await collection().find_one_and_update(
        {
            "id": memory_id,
            "userId": user["id"]
        },
        {"$set": updates},
        return_document=True,
        projection={"_id": 0, "userId": 0}
    )

    if result is None:
        raise HTTPException(404, "Memory not found")

    return result


@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: str,
    user=Depends(current_user)
):
    result = await collection().delete_one({
        "id": memory_id,
        "userId": user["id"]
    })

    if result.deleted_count == 0:
        raise HTTPException(404, "Memory not found")

    return {"message": "Memory deleted"}

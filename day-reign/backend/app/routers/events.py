from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.database import get_database
from app.models.event import EventInput, EventResponse

router = APIRouter(prefix="/api/events", tags = ["Events"])

def collection():
    return get_database()["events"]

@router.get("", response_model = list[EventResponse])
async def list_events():
    cursor = collection().find(
        {},
        {"_id": 0}
    ).sort([("date", 1), ("startTime", 1)]) 

    return await cursor.to_list(length=1000)

@router.post("", response_model = EventResponse, status_code=201)
async def create_event(event: EventInput):
    document = {
        "id": str(uuid4()),
        **event.model_dump()
    }

    await collection().insert_one(document)

    return document

@router.patch("/{event_id}", response_model = EventResponse)
async def update_event(event_id: str, event: EventInput):
    result = await collection().find_one_and_update(
        {"id": event_id},
        {"$set": event.model_dump()},
        return_document = True,
        projection={"_id": 0}
    )

    if result is None:
        raise HTTPException(404, "Event Not Found")

    return result

@router.delete("/{event_id}")
async def delete_event(event_id: str):
    result = await collection().delete_one({"id": event_id})

    if result.deleted_count == 0:
        raise HTTPException(404, "Event Not Found")

    return {"message": "Event deleted"}
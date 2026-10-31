from typing import Literal
from pydantic import BaseModel, Field, model_validator

Category = Literal[
    "Personal", "School", "Work", "Health", "Other"
]

class EventInput(BaseModel):
    title: str = Field(min_length = 1, max_length = 120)
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    startTime : str = ""
    endTime : str = ""
    allDay: bool = False
    category: Category = "Personal"
    description: str = Field(default="", max_length=2000)

    @model_validator(mode="after")
    def validate_event(self):
        from datetime import date as Date, time as Time

        Date.fromisoformat(self.date)

        if not self.allDay:
            if not self.startTime or not self.endTime:
                raise ValueError("Start and end time are required")

            start = Time.fromisoformat(self.startTime)
            end = Time.fromisoformat(self.endTime)

            if end <= start:
                raise ValueError("End time must be after start time")
        else:
            self.startTime = ""
            self.endTime = ""

        self.title = self.title.strip()

        if not self.title:
            raise ValueError("Title cannot be empty")
        return self

class EventResponse(EventInput):
    id: str
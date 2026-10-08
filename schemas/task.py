from typing import TypedDict

from pydantic import BaseModel, Field


class Task(TypedDict):
    id: int
    title: str
    priority: int


class TaskIn(BaseModel):
    title: str
    priority: int = Field(default=1, ge=1, le=5)


class TaskPatch(BaseModel):
    title: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)

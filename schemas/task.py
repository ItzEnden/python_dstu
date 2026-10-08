from pydantic import BaseModel, ConfigDict, Field


class TaskIn(BaseModel):
    title: str
    priority: int = Field(default=1, ge=1, le=5)


class TaskPatch(BaseModel):
    title: str | None = None
    priority: int | None = Field(default=None, ge=1, le=5)


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    priority: int

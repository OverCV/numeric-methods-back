from pydantic import BaseModel, Field
from typing import Optional, List


class GraphRequest(BaseModel):
    title: str

    image_url: str
    error_url: str

    solution: float


class GraphCreate(GraphRequest):
    pass


class GraphUpdate(GraphRequest):
    pass


class GraphResponse(GraphRequest):
    approximation_id: int
    id: int

    class Config:
        orm_mode = True

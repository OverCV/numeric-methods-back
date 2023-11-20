from pydantic import BaseModel, Field
from typing import Optional, List


class ConstantRequest(BaseModel):
    name: str
    value: float


class ConstantCreate(ConstantRequest):
    pass


class ConstantUpdate(ConstantRequest):
    pass


class ConstantResponse(ConstantRequest):
    id: int
    approximation_id: int

    class Config:
        orm_mode = True

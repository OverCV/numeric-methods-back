from pydantic import BaseModel, Field
from typing import Optional, List


class BaseConstant(BaseModel):
    name: str
    value: float


class ConstantCreate(BaseConstant):
    pass


class ConstantUpdate(BaseConstant):
    pass


class ConstantRead(BaseConstant):
    id: int
    approximation_id: int

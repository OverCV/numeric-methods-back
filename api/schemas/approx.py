from pydantic import BaseModel, Field
from models.base import Approximation, Graph
from typing import Optional, List

from schemas.constant import ConstantResponse
from schemas.graph import GraphResponse
from constants.const import *


class ApproxRequest(BaseModel):
    title: str
    f: str

    ind_var: str
    ind_value: float

    dep_var: str
    dep_value: float

    eval_value: float

    h: float
    N: int

    


class ApproxCreate(ApproxRequest):
    pass


class ApproxUpdate(ApproxRequest):
    pass


class ApproxResponse(ApproxRequest):
    id: int

    # graphs: List[GraphResponse] = []
    # constants: List[ConstantResponse] = []

    class Config:
        orm_mode = True

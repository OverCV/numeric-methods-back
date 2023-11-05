from pydantic import BaseModel, Field
from typing import Optional, List

from schemas.constant import ConstantRead
from schemas.graph import GraphRead
from constants.const import *


class BaseApprox(BaseModel):
    title: str

    t0: float
    x0: float
    t: float

    h: float
    N: int


class ApproxCreate(BaseApprox):
    pass


class ApproxUpdate(BaseModel):
    title: str
    f: str

    t0: float
    x0: float
    t: float

    h: float
    N: int


class ApproxRead(BaseApprox):
    x: float
    f: str
    id: int

    constants: List[ConstantRead] = []
    graphs: List[GraphRead] = []

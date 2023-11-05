from pydantic import BaseModel, Field
from typing import Optional, List

from schemas.constant import ConstantRead
from schemas.graph import GraphRead


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
    func: str

    t0: float
    x0: float
    t: float

    h: float
    N: int


class ApproxRead(BaseApprox):
    x: float
    func: str
    id: int

    constants: List[ConstantRead] = []
    graphs: List[GraphRead] = []

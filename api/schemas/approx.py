from pydantic import BaseModel, Field
from typing import Optional, List

from schemas.constant import ConstantRead
from schemas.graph import GraphRead
from constants.const import *


class BaseApprox(BaseModel):
    title: str
    f: str

    ind_var: str
    ind_value: float

    dep_var: str
    dep_value: float

    eval_value: float

    h: float
    N: int


class ApproxCreate(BaseApprox):
    pass


class ApproxUpdate(BaseApprox):
    pass


class ApproxRead(BaseApprox):
    result: float
    f: str
    id: int

    constants: List[ConstantRead] = []
    graphs: List[GraphRead] = []

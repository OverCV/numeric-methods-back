from pydantic import BaseModel, Field
from typing import Optional, List


class EulerBase(BaseModel):
    title: str

    t0: Optional[float]
    x0: Optional[float]
    t: Optional[float]

    a: Optional[float]
    N: float


class EulerCreate(EulerBase):
    pass


class EulerUpdate(BaseModel):
    title: str
    func: str

    t0: Optional[float]
    x0: Optional[float]
    t: Optional[float]

    a: Optional[float]
    N: float


class EulerSchema(EulerBase):
    euler_graph_url: str
    euler_error_url: str

    x: float
    func: str
    id: int

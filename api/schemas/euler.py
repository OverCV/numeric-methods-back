from pydantic import BaseModel, Field
from typing import Optional, List


class EulerBase(BaseModel):
    title: str

    t0: Optional[float] = Field(default=0.0)
    x0: Optional[float] = Field(default=0.0)
    t: Optional[float] = Field(default=0.0)

    a: Optional[float] = Field(default=0.0)
    N: float


class EulerCreate(EulerBase):
    pass


class EulerUpdate(BaseModel):
    title: str
    func: str

    t0: Optional[float] = Field(default=0.0)
    x0: Optional[float] = Field(default=0.0)
    t: Optional[float] = Field(default=0.0)

    a: Optional[float] = Field(default=0.0)
    N: float


class EulerSchema(EulerBase):
    id: int
    x: float

    euler_graph_url: str
    euler_error_url: str

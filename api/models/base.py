from typing import Optional
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey

from database.db import Base
from constants.const import *


class Euler(Base):
    __tablename__ = 'euler'
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title: str = Column(String(63), nullable=False)
    func: str = Column(String(255), nullable=False, default=EULER_FUNCTION)

    t0: float = Column(Integer, nullable=False, default=0.0)
    x0: float = Column(Integer, nullable=False, default=0.0)
    t: float = Column(Integer, nullable=False, default=0.0)
    x: float = Column(Integer, default=0.0)

    a: float = Column(Integer, nullable=False, default=0.0)
    N: float = Column(Integer, nullable=False, default=0.0)

    euler_graph_url: str = Column(String(255), nullable=True)
    euler_error_url: str = Column(String(255), nullable=True)

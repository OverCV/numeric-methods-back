from typing import Optional
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, String, ForeignKey, Float
)

from database.db import Base
from constants.const import *


class Approximation(Base):
    __tablename__ = 'approximations'
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(63), nullable=False)

    f = Column(String(255), default=EXP_FUNCTION)

    t0: float = Column(Float, default=0.0)
    x0: float = Column(Float, default=0.0)
    t: float = Column(Float, default=0.0)
    x: float = Column(Float, default=0.0)

    a: float = Column(Float, default=0.0)
    h: float = Column(Float, default=0.0)
    N: int = Column(Integer, default=0.0)

    constants = relationship('Constant', back_populates='approximation')
    graphs = relationship('Graph', back_populates='approximation')


class Constant(Base):
    __tablename__ = 'constants'
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String(31), nullable=False)
    value: int = Column(Float, default=0.0)

    approximation_id = Column(Integer, ForeignKey('approximations.id'))
    approximation = relationship('Approximation', back_populates='constants')


class Graph(Base):
    __tablename__ = 'graphs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(63), nullable=False)

    image_url = Column(String(255), default='')
    error_url = Column(String(255), default='')

    approximation_id = Column(Integer, ForeignKey('approximations.id: int'))
    approximation = relationship('Approximation', back_populates='graphs')

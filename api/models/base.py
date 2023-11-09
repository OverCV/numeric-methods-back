from typing import Optional
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Table, Column, Integer, String, Boolean, ForeignKey, Float
)

from database.db import Base
from constants.const import *


class Approximation(Base):
    __tablename__ = 'approximations'
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    f: str = Column(String(255), default=EXP_FUNCTION)

    result: float = Column(Float, default=0.0)

    title = Column(String(63), default=f'Approximation {id}')

    ind_var: str = Column(String(31), default='t0')
    ind_value: float = Column(Float)

    dep_var: str = Column(String(31), default='x0')
    dep_value: float = Column(Float)

    eval_value: float = Column(Float)

    # x0: float = Column(Float)
    # t: float = Column(Float)

    h: float = Column(Float)
    N: int = Column(Integer)

    constants = relationship('Constant', back_populates='approximation')
    graphs = relationship('Graph', back_populates='approximation')


class Constant(Base):
    __tablename__ = 'constants'
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String(31), nullable=False)
    value: int = Column(Float)

    approximation_id = Column(Integer, ForeignKey('approximations.id'))
    approximation = relationship('Approximation', back_populates='constants')


class Graph(Base):
    __tablename__ = 'graphs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(63), nullable=False)

    image_url = Column(String(255))
    error_url = Column(String(255))

    approximation_id = Column(Integer, ForeignKey('approximations.id'))
    approximation = relationship('Approximation', back_populates='graphs')

from typing import Optional
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Table, Column, Integer, String, Boolean, ForeignKey, Float
)

from database.db import Base
from constants.const import EXP_FUNCTION


class Approximation(Base):
    __tablename__ = 'approximations'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    f: str = Column(String(255), default=EXP_FUNCTION)

    title = Column(String(63), default=f'Approximation {id}')

    ind_var: str = Column(String(31), default='t0')
    ind_value: float = Column(Float)

    dep_var: str = Column(String(31), default='x0')
    dep_value: float = Column(Float)

    eval_value: float = Column(Float)

    h: float = Column(Float)
    N: int = Column(Integer)

    constants = relationship(
        'Constant', back_populates='approximation', uselist=True,
        cascade='all, delete-orphan'
    )
    graphs = relationship(
        'Graph', back_populates='approximation',
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Constant(Base):
    __tablename__ = 'constants'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(31), nullable=False)
    value: float = Column(Float, default=0.0)

    approximation_id: int = Column(Integer, ForeignKey('approximations.id'))
    approximation = relationship('Approximation', back_populates='constants')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Graph(Base):
    __tablename__ = 'graphs'
    id: int = Column(Integer, primary_key=True, autoincrement=True)

    title: str = Column(String(63), nullable=False)
    solution: float = Column(Float, default=0.0)

    image_url: str = Column(String(255))
    error_url: str = Column(String(255))

    approximation_id: int = Column(
        Integer, ForeignKey('approximations.id'), nullable=True
    )
    approximation = relationship('Approximation', back_populates='graphs',)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

from sqlalchemy.orm import Session
from models.base import Euler
from schemas.euler import EulerCreate, EulerUpdate, EulerSchema
from typing import List


def create_euler(euler: EulerCreate, db: Session) -> EulerSchema:
    db_euler: Euler = Euler(**euler.model_dump())
    db.add(db_euler)
    db.commit()
    db.refresh(db_euler)
    return EulerSchema(**db_euler.model_dump())


def read_eulers(db: Session) -> List[EulerSchema]:
    db_eulers: List[Euler] = db.query(Euler).all()
    return [EulerSchema(**euler.model_dump()) for euler in db_eulers]


def read_euler(euler_id: int, db: Session) -> EulerSchema:
    db_euler: Euler = db.query(Euler).filter(
        Euler.id == euler_id
    ).first()
    return EulerSchema(**db_euler.model_dump())


def update_euler(euler_id: int, euler: EulerUpdate, db: Session) -> EulerSchema:
    db_euler: Euler = db.query(Euler).filter(
        Euler.id == euler_id
    ).first()
    for attr, value in vars(euler).items():
        setattr(db_euler, attr, value)  # if value else None
    db.commit()
    db.refresh(db_euler)
    return EulerSchema(**db_euler.model_dump())


def remove_euler(euler_id: int, db: Session) -> EulerSchema:
    db_euler: Euler = db.query(Euler).filter(
        Euler.id == euler_id
    ).first()
    db.delete(db_euler)
    db.commit()
    return EulerSchema(**db_euler.model_dump())


def exist_euler_title(title: str, db: Session) -> bool:
    db_euler: Euler = db.query(Euler).filter(
        Euler.title == title
    ).first()
    return False if db_euler is None else True


def exist_euler_id(euler_id: int, db: Session) -> bool:
    db_euler: Euler = db.query(Euler).filter(
        Euler.id == euler_id
    ).first()
    return False if db_euler is None else True

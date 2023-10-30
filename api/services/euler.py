from sqlalchemy.orm import Session
from models.base import Euler
from schemas.euler import EulerCreate, EulerUpdate, EulerSchema
from typing import List


def create_euler(euler: EulerCreate, db: Session) -> EulerSchema:
    db_euler: Euler = Euler(**euler.model_dump())
    db.add(db_euler)
    db.commit()
    db.refresh(db_euler)
    return EulerSchema(**db_euler.__dict__)


def read_eulers(db: Session) -> List[EulerSchema]:
    db_eulers: List[Euler] = db.query(Euler).all()
    return [EulerSchema(**euler.__dict__) for euler in db_eulers]


def read_euler(euler_id: int, db: Session) -> EulerSchema:
    db_euler: Euler = db.query(Euler).filter(
        Euler.id == euler_id
    ).first()
    return EulerSchema(**db_euler.__dict__)


def replace_euler(euler_id: int, euler: EulerUpdate, db: Session) -> EulerSchema:
    db_euler: Euler = db.query(Euler).filter(
        Euler.id == euler_id
    ).first()
    for key, value in euler.model_dump().items():
        setattr(db_euler, key, value)
    db.commit()
    db.refresh(db_euler)

    return EulerSchema(**db_euler.__dict__)


def update_euler(euler_id: int, euler: EulerUpdate, db: Session) -> EulerSchema:
    db_euler: Euler = db.query(Euler).filter(
        Euler.id == euler_id
    ).first()
    for key, value in euler.model_dump().items():
        if (value is not None) or (value != ''):
            setattr(db_euler, key, value)
    db.commit()
    db.refresh(db_euler)

    return EulerSchema(**db_euler.__dict__)


def remove_euler(euler_id: int, db: Session) -> EulerSchema:
    db_euler: Euler = db.query(Euler).filter(
        Euler.id == euler_id
    ).first()
    db.delete(db_euler)
    db.commit()
    return EulerSchema(**db_euler.__dict__)


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

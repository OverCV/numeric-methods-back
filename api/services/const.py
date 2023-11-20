from sqlalchemy.orm import Session
from models.base import Constant, Approximation
from schemas.constant import ConstantCreate, ConstantResponse, ConstantUpdate

from fastapi import status
from typing import List

# from services.approx import exist_approx_id


def create_const(approx_id: int, const: ConstantCreate, db: Session) -> ConstantResponse:
    if exist_name_by_id(const.name, approx_id, db):
        return None, status.HTTP_409_CONFLICT

    if related_names(const.name, approx_id, db):
        return None, status.HTTP_406_NOT_ACCEPTABLE

    db_const: Constant = Constant(**const.dict())
    db_const.approximation_id = approx_id

    db.add(db_const)
    db.commit()
    db.refresh(db_const)
    return ConstantResponse(**db_const.__dict__), status.HTTP_201_CREATED


def read_const(const_id: int, db: Session) -> ConstantResponse:
    db_const: Constant = db.query(Constant).filter(
        Constant.id == const_id
    ).first()
    if db_const is None:
        return None, status.HTTP_404_NOT_FOUND
    return ConstantResponse(**db_const.__dict__), status.HTTP_200_OK


def read_consts(db: Session) -> List[ConstantResponse]:
    db_consts: List[Constant] = db.query(Constant).all()
    return [ConstantResponse(**const.__dict__) for const in db_consts]


def update_const(const_id: int, const: ConstantUpdate, db: Session) -> ConstantResponse:
    db_const: Constant = db.query(Constant).filter(
        Constant.id == const_id
    ).first()
    if db_const is None:
        return None, status.HTTP_404_NOT_FOUND

    db_const.name, db_const.value = const.name, const.value

    db.commit()
    db.refresh(db_const)
    return ConstantResponse(**db_const.__dict__), status.HTTP_202_ACCEPTED


def remove_const(const_id: int, db: Session) -> ConstantResponse:
    db_const: Constant = db.query(Constant).filter(
        Constant.id == const_id
    ).first()
    if db_const is None:
        return None, status.HTTP_404_NOT_FOUND

    db.delete(db_const)
    db.commit()
    return ConstantResponse(**db_const.__dict__), status.HTTP_202_ACCEPTED


def exist_name_by_id(const_name: str, approx_id: int, db: Session) -> bool:
    count = db.query(Constant.approximation_id).filter(
        Constant.approximation_id == approx_id,
        Constant.name == const_name
    ).group_by(Constant.name).count()

    # Si count es mayor que 0, entonces existen constantes con ese nombre
    return count > 0


def related_names(const_name: str, approx_id: int, db: Session) -> bool:
    db_approx: Approximation = db.query(Approximation).filter(
        Approximation.id == approx_id
    ).first()

    return db_approx.dep_var == const_name\
        or db_approx.ind_var == const_name

# def exist_const_id(const_id: int, db: Session) -> bool:
#     db_const: Constant = db.query(Constant).filter(
#         Constant.id == const_id
#     ).first()
#     return False if db_const is None else True

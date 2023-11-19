from typing import List
from sqlalchemy.orm import Session
from models.base import Approximation, Constant
from services.core.constants import get_consts_dict
import re


def exist_approx_id(approx_id: int, db: Session) -> bool:
    db_approx: Approximation = db.query(Approximation).filter(
        Approximation.id == approx_id
    ).first()
    return False if db_approx is None else True


def exist_approx_const_title(approx: Approximation, db: Session) -> bool:
    consts: List[Constant] = db.query(Constant).filter(
        Constant.approximation_id == approx.id,
    ).all()
    for const in consts:
        if const.name == approx.dep_var\
                or const.name == approx.ind_var:
            return True
    return False


def exist_approx_title(title: str, db: Session) -> bool:
    db_approx: Approximation = db.query(Approximation).filter(
        Approximation.title == title
    ).first()
    return False if db_approx is None else True


def validations(approx: Approximation, db: Session) -> bool:
    consts = get_consts_dict(approx.id, db)
    chars: list[str] = approx.f.split(' ')

    for key in consts.keys():
        if key not in chars:
            return False

    for char in chars:
        if not re.match(r'^[a-zA-Z]+\d+$', char):
            continue
        if char not in consts.keys():
            return False

    return True

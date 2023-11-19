from typing import List
from sqlalchemy.orm import Session
from models.base import Approximation, Constant
from services.core.constants import get_consts_dict
from constants.const import REGEX
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


def validate_consts(approx: Approximation, db: Session) -> bool:

    consts = get_consts_dict(approx.id, db)
    tokens = re.findall(REGEX, approx.f)

    for cte in consts.keys():
        if cte not in tokens:
            return False

    return True


def validate_vars(approx: Approximation) -> bool:
    chars: list[str] = extract_variables(approx.f)
    return (approx.dep_var in chars) and (approx.ind_var in chars)


def extract_variables(expression):
    exclude = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'e', 'E', 'pi', 'PI']
    tokens = re.findall(REGEX, expression)
    variables = [word for word in tokens if word not in exclude]

    return variables

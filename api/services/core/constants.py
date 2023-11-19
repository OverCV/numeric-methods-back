from models.base import Constant
from sqlalchemy.orm import Session

from schemas.constant import ConstantResponse
from typing import List


def get_consts_dict(approx_id: int, db: Session) -> dict[str, float]:
    consts: List[Constant] = read_consts(approx_id, db)
    return {const.name: const.value for const in consts}


def read_consts(approx_id: int, db: Session) -> List[ConstantResponse]:
    db_consts: List[Constant] = db.query(Constant).filter(
        Constant.approximation_id == approx_id
    ).all()
    return [ConstantResponse(**const.__dict__) for const in db_consts]

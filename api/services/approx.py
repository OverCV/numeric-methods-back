from sqlalchemy.orm import Session
from typing import List
from fastapi import status

from models.base import Approximation, Graph
from schemas.graph import GraphCreate, GraphResponse
from schemas.approx import ApproxCreate, ApproxResponse, ApproxUpdate
from constants.const import *

from services.core import methods

from services.validators import helper as vh
from services.core import constants, graphicate


def create_approx(approximation: ApproxCreate, db: Session) -> ApproxResponse:
    if vh.exist_approx_title(approximation.title, db):
        return None
    db_approx: Approximation = Approximation(**approximation.model_dump())

    if db_approx.f == '' or db_approx.f is None:
        db_approx.f: str = f'{db_approx.dep_var} + E**({db_approx.ind_var})'

    db.add(db_approx)
    db.commit()
    db.refresh(db_approx)
    return ApproxResponse(**db_approx.__dict__)


def read_approxs(db: Session) -> List[ApproxResponse]:
    db_approxs: List[Approximation] = db.query(Approximation).all()
    return [ApproxResponse(**approx.__dict__) for approx in reversed(db_approxs)]


def read_approx(approx_id: int, db: Session) -> ApproxResponse:
    db_approx: Approximation = db.query(Approximation).filter(
        Approximation.id == approx_id
    ).first()
    return ApproxResponse(**db_approx.__dict__)


def replace_approx(approx_id: int, approx: ApproxUpdate, db: Session) -> ApproxResponse:
    if not vh.exist_approx_id(approx_id, db):
        return None

    db_approx: Approximation = db.query(Approximation).filter(
        Approximation.id == approx_id
    ).first()

    for key, value in approx.model_dump().items():
        setattr(db_approx, key, value)

    if db_approx.f == '' or db_approx.f is None:
        db_approx.f: str = f'{db_approx.dep_var} + E**({db_approx.ind_var})'

    db.commit()
    db.refresh(db_approx)

    return ApproxResponse(**db_approx.__dict__)


def update_approx(approx_id: int, approximation: ApproxUpdate, db: Session) -> ApproxResponse:
    db_approx: Approximation = db.query(Approximation).filter(
        Approximation.id == approx_id
    ).first()

    if not vh.exist_approx_id(approx_id, db):
        return None

    if vh.exist_approx_const_title(approximation, db):
        return None

    for key, value in db_approx.model_dump().items():
        if (value is None) or (value == ''):
            setattr(db_approx, approximation[key], approximation[value])
    db.commit()
    db.refresh(db_approx)

    return ApproxResponse(**db_approx.__dict__)


def remove_approx(approx_id: int, db: Session) -> bool:
    if not vh.exist_approx_id(approx_id, db):
        return False
    db_approx: Approximation = db.query(Approximation).filter(
        Approximation.id == approx_id
    ).first()

    for graph in db_approx.graphs:
        db.delete(graph)

    for const in db_approx.constants:
        db.delete(const)

    db.delete(db_approx)
    db.commit()
    return True


def read_graphs(approx_id: int, db: Session) -> List[GraphResponse]:
    db_graphs: List[Graph] = db.query(Graph).filter(
        Graph.approximation_id == approx_id
    ).all()
    return [GraphResponse(**graph.__dict__) for graph in db_graphs]


def create_graphs(approx_id: int, db: Session) -> int:
    if not vh.exist_approx_id(approx_id, db):
        return status.HTTP_404_NOT_FOUND

    db_approx: Approximation = db.query(Approximation).filter(
        Approximation.id == approx_id
    ).first()

    if db_approx is None:
        return status.HTTP_404_NOT_FOUND

    validated: bool = vh.validations(db_approx, db)
    if not validated:
        return status.HTTP_409_CONFLICT

    consts: dict[str, float] = constants.get_consts_dict(approx_id, db)
    # IND: np.linspace = np.linspace(
    #     db_approx.ind_value, db_approx.eval_value, db_approx.N
    # )

    euler_data: dict[str, list[float]]\
        = methods.euler_approx(db_approx, consts)

    rk2_data: dict[str, list[float]]\
        = methods.rk2_approx(db_approx, consts)

    rk4_data: tuple[list[float], list[float]]\
        = methods.rk4_approx(db_approx, consts)

    # rk45_data: tuple[list[float], list[float]] =\
    #     rk45_approx(
    #     db_approx.f, db_approx.dep_var, db_approx.ind_var,
    #     db_approx.dep_value, IND, consts
    # )

    methods_data: dict[str, dict[str, list[float]]] = {
        'euler': euler_data,
        'rk2': rk2_data,
        'rk4': rk4_data
    }

    # ? Asociate the graphs to the approximation ? #

    graphs_generated: dict[str: GraphCreate] = None

    graphs_generated = graphicate.generate_graphs(
        db_approx, methods_data
    )

    if graphs_generated is None:
        return status.HTTP_304_NOT_MODIFIED

    return status.HTTP_201_CREATED

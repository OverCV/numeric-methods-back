from sqlalchemy.orm import Session
from models.base import Approximation as Approx
from schemas.approx import ApproxCreate, ApproxRead, ApproxUpdate
from typing import List
# from constants.const import approx_method
import matplotlib.pyplot as plt


def create_approx(approx: ApproxCreate, db: Session) -> ApproxRead:
    db_approx: Approx = Approx(**approx.model_dump())

    if exist_approx_title(approx.title, db):
        return None

    db.add(db_approx)
    db.commit()
    db.refresh(db_approx)
    return ApproxRead(**db_approx.__dict__)


def read_approxs(db: Session) -> List[ApproxRead]:
    db_approxs: List[Approx] = db.query(Approx).all()
    return [ApproxRead(**approx.__dict__) for approx in db_approxs]


def read_approx(approx_id: int, db: Session) -> ApproxRead:
    db_approx: Approx = db.query(Approx).filter(
        Approx.id == approx_id
    ).first()
    return ApproxRead(**db_approx.__dict__)


def replace_approx(approx_id: int, approx: ApproxUpdate, db: Session) -> ApproxRead:
    db_approx: Approx = db.query(approx).filter(
        approx.id == approx_id
    ).first()

    if not exist_approx_id(approx_id, db):
        return None

    for key, value in approx.model_dump().items():
        setattr(db_approx, key, value)
    db.commit()
    db.refresh(db_approx)

    return ApproxRead(**db_approx.__dict__)


def update_approx(approx_id: int, approx: ApproxUpdate, db: Session) -> ApproxRead:
    db_approx: Approx = db.query(approx).filter(
        approx.id == approx_id
    ).first()

    if not exist_approx_id(approx_id, db):
        return None

    for key, value in approx.model_dump().items():
        if (value is not None) or (value != ''):
            setattr(db_approx, key, value)
    db.commit()
    db.refresh(db_approx)

    return ApproxRead(**db_approx.__dict__)


def remove_approx(approx_id: int, db: Session) -> ApproxRead:
    if not exist_approx_id(approx_id, db):
        return None

    db_approx: Approx = db.query(Approx).filter(
        Approx.id == approx_id
    ).first()
    db.delete(db_approx)
    db.commit()
    return ApproxRead(**db_approx.__dict__)


def exist_approx_title(title: str, db: Session) -> bool:
    db_approx: Approx = db.query(Approx).filter(
        Approx.title == title
    ).first()
    return False if db_approx is None else True


def exist_approx_id(approx_id: int, db: Session) -> bool:
    db_approx: Approx = db.query(Approx).filter(
        Approx.id == approx_id
    ).first()
    return False if db_approx is None else True


""" approx core algorithm """


def calculate_approx(approx: Approx) -> None:
    h = (approx.t - approx.t0) / approx.N
    t = approx.t0
    x = approx.x0
    approx.T = [t]
    approx.X = [x]
    for i in range(int(approx.N)):
        # x += h * approx_method(approx.func, t, x)
        t += h
        approx.T.append(t)
        approx.X.append(x)


# def approx_method_algorithm(approx: Approx) -> List[float]:
#     h = (approx.t - approx.t0) / approx.N
#     t = approx.t0
#     x = approx.x0
#     approx_graph = [x]
#     for i in range(int(approx.N)):
#         x += h * approx_method(approx.func, t, x)
#         t += h
#         approx_graph.append(x)
#     return approx_graph


# def calculate_approx_error(approx: Approx, approx_graph: List[float]) -> List[float]:
#     h = (approx.t - approx.t0) / approx.N
#     t = approx.t0
#     x = approx.x0
#     approx_error = []
#     for i in range(int(approx.N)):
#         x += h * approx_method(approx.func, t, x)
#         t += h
#         approx_error.append(abs(x - approx_graph[i]))
#     return approx_error


# def plot_approx_graph(approx_graph: List[float], approx: Approx) -> None:
#     plt.plot([i for i in range(int(approx.N) + 1)], approx_graph)
#     plt.title(f"approx Method Graph for {approx.title}")
#     plt.xlabel("Steps")
#     plt.ylabel("Approximated Solution")
#     plt.show()


# def plot_approx_error(approx_error: List[float], approx: Approx) -> None:
#     plt.plot([i for i in range(int(approx.N))], approx_error)
#     plt.title(f"approx Method Error Graph for {approx.title}")
#     plt.xlabel("Steps")
#     plt.ylabel("Error")
#     plt.show()


# def plot_approx(approx: Approx) -> None:
#     approx_graph = eval(approx.approx_graph_url)
#     approx_error = eval(approx.approx_error_url)
#     plot_approx_graph(approx_graph, approx)
#     plot_approx_error(approx_error, approx)



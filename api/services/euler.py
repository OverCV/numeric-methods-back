from sqlalchemy.orm import Session
from models.base import Euler
from schemas.euler import EulerCreate, EulerUpdate, EulerSchema
from typing import List
# from constants.const import euler_method
import matplotlib.pyplot as plt


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


def create_euler(euler: EulerCreate, db: Session) -> EulerSchema:
    # euler_graph = euler_method_algorithm(euler)
    # euler_error = calculate_euler_error(euler, euler_graph)
    db_euler: Euler = Euler(
        **euler.model_dump(),
        # euler_graph_url=str(euler_graph),
        # euler_error_url=str(euler_error)
    )
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
    # euler_graph = euler_method_algorithm(db_euler)
    # euler_error = calculate_euler_error(db_euler, euler_graph)
    # db_euler.euler_graph_url = str(euler_graph)
    # db_euler.euler_error_url = str(euler_error)
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


""" Euler core algorithm """


# def euler_method_algorithm(euler: Euler) -> List[float]:
#     h = (euler.t - euler.t0) / euler.N
#     t = euler.t0
#     x = euler.x0
#     euler_graph = [x]
#     for i in range(int(euler.N)):
#         x += h * euler_method(euler.func, t, x)
#         t += h
#         euler_graph.append(x)
#     return euler_graph


# def calculate_euler_error(euler: Euler, euler_graph: List[float]) -> List[float]:
#     h = (euler.t - euler.t0) / euler.N
#     t = euler.t0
#     x = euler.x0
#     euler_error = []
#     for i in range(int(euler.N)):
#         x += h * euler_method(euler.func, t, x)
#         t += h
#         euler_error.append(abs(x - euler_graph[i]))
#     return euler_error


# def plot_euler_graph(euler_graph: List[float], euler: Euler) -> None:
#     plt.plot([i for i in range(int(euler.N) + 1)], euler_graph)
#     plt.title(f"Euler Method Graph for {euler.title}")
#     plt.xlabel("Steps")
#     plt.ylabel("Approximated Solution")
#     plt.show()


# def plot_euler_error(euler_error: List[float], euler: Euler) -> None:
#     plt.plot([i for i in range(int(euler.N))], euler_error)
#     plt.title(f"Euler Method Error Graph for {euler.title}")
#     plt.xlabel("Steps")
#     plt.ylabel("Error")
#     plt.show()


# def plot_euler(euler: Euler) -> None:
#     euler_graph = eval(euler.euler_graph_url)
#     euler_error = eval(euler.euler_error_url)
#     plot_euler_graph(euler_graph, euler)
#     plot_euler_error(euler_error, euler)

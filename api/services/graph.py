from sqlalchemy.orm import Session
from models.base import Graph
from schemas.graph import GraphCreate, GraphResponse, GraphUpdate
from typing import List


# def instance_graph(graph: GraphCreate, db: Session) -> Graph:
#     if exist_graph_title(graph.title, approx_id, db):
#         return None

#     db_graph: Graph = Graph(**graph.dict())

#     db.add(db_graph)
#     db.commit()
#     db.refresh(db_graph)
#     return db_graph


def create_graph(graph: GraphCreate, approx_id: int, db: Session) -> GraphResponse:
    if exist_graph_title(graph.title, approx_id, db):
        return None

    db_graph: Graph = Graph(
        **graph.dict(),
        approximation_id=approx_id
    )

    db.add(db_graph)
    db.commit()
    db.refresh(db_graph)
    return GraphResponse(**db_graph.__dict__)


def read_graphs(db: Session) -> List[GraphResponse]:
    db_graphs: List[Graph] = db.query(Graph).all()
    return [GraphResponse(**graph.__dict__) for graph in db_graphs]


def read_graph(graph_id: int, db: Session) -> Graph:
    db_graph: Graph = db.query(Graph).filter(
        Graph.id == graph_id
    ).first()
    return Graph(**db_graph.__dict__)


def drop_graph(graph_id: int, db: Session) -> bool:
    if not exist_graph_id(graph_id, db):
        return False

    db_graph: Graph = db.query(Graph).filter(
        Graph.id == graph_id
    ).first()

    if db_graph is None:
        return False

    db.delete(db_graph)
    db.commit()
    return True

def drop_graphs(approx_id: int, db: Session) -> bool:
    if not have_graphs(approx_id, db):
        return False

    db_graphs: List[Graph] = db.query(Graph).filter(
        Graph.approximation_id == approx_id
    ).all()

    if db_graphs is None:
        return False

    for graph in db_graphs:
        db.delete(graph)
    db.commit()
    return True

def exist_graph_id(approx_id: int, db: Session) -> bool:
    db_graph: Graph = db.query(Graph).filter(
        Graph.id == approx_id
    ).first()
    return False if db_graph is None else True


def exist_graph_title(graph_title: str, id_approx: int, db: Session) -> bool:
    db_graph: Graph = db.query(Graph).filter(
        Graph.title == graph_title,
        Graph.approximation_id == id_approx
    ).first()
    return False if db_graph is None else True

def have_graphs(approx_id: int, db: Session) -> bool:
    db_graphs: List[Graph] = db.query(Graph).filter(
        Graph.approximation_id == approx_id
    ).all()
    return False if db_graphs is None else True
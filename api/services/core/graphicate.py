from fastapi import status
from models.base import Approximation, Graph
from schemas.graph import GraphCreate, GraphResponse
from services.plot import store_graph
from services.graph import create_graph
from constants.const import *
from typing import List
from sqlalchemy.orm import Session


def generate_graphs(
    approx: Approximation,
    datasource: dict[str, dict[str, list[float]]],
    db: Session,
    graphs_data: list = []
) -> dict[str: GraphCreate]:
    for method_key, data in datasource.items():
        image_path: str | None = store_graph(
            approx.id,
            method_key, 'image',
            approx.ind_var, data[IND_KEY],
            approx.dep_var, data[DEP_KEY],
            approx.f
        )

        error_path: str | None = store_graph(
            approx.id,
            method_key, 'error',
            approx.ind_var, data[IND_KEY],
            approx.dep_var, data[ERR_KEY],
            approx.f
        )

        if image_path is None or error_path is None:
            return status.HTTP_409_CONFLICT

        graph = GraphCreate(
            title=method_key,
            image_url=image_path,
            error_url=error_path,
            approximation_id=approx.id,
            solution=data[DEP_KEY][-1]
        )
        # Crear directamente la instancia de Graph
        responsed_graph: GraphResponse = create_graph(
            graph, approx.id, db
        )
        graphs_data.append(responsed_graph)

    return graphs_data

    # # db_graph = Graph(**euler_graph, approximation_id=db_approx.id)

    # # Asociar el Graph con Approximation
    # db_approx.graphs.append(responsed_graph)
    # db.commit()
    # db.refresh(db_approx)

    # print(db_approx.graphs)  # Verificar la asociación

    # return ApproxRead(**db_approx.__dict__), status.HTTP_201_CREATED


def relate_graphs(approx: Approximation, new_graphs: list[GraphResponse], db: Session):
    if new_graphs is None:
        return None, status.HTTP_410_GONE

    approx.graphs: List[Graph] = new_graphs
    db.commit()
    db.refresh(approx)

    return approx, status.HTTP_200_OK


def read_graphs(approx_id: int, db: Session) -> List[GraphResponse]:
    db_graphs: List[Graph] = db.query(Graph).filter(
        Graph.approximation_id == approx_id
    ).all()
    return [GraphResponse(**graph.__dict__) for graph in db_graphs]

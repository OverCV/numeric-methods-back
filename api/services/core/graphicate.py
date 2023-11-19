from fastapi import status
from models.base import Approximation
from schemas.graph import GraphCreate
from services.plot import store_graph
from constants.const import *


def generate_graphs(
    approx: Approximation, datasource: dict[str, dict[str, list[float]]],
    data_graphs: dict[str: GraphCreate] = {}
) -> dict[str: GraphCreate]:
    for key, data in datasource.items():
        image_path: str | None = store_graph(
            approx.id,
            key, 'image',
            approx.ind_var, data[IND_KEY],
            approx.dep_var, data[DEP_KEY],
            approx.f
        )

        error_path: str | None = store_graph(
            approx.id,
            key, 'error',
            approx.ind_var, data[IND_KEY],
            approx.dep_var, data[ERR_KEY],
            approx.f
        )

        if image_path is None or error_path is None:
            return status.HTTP_409_CONFLICT

        graph = GraphCreate(
            title=f'Euler {approx.title} Graph',
            image_url=image_path,
            error_url=error_path,
            approximation_id=approx.id,
            solution=data[DEP_KEY][-1]
        )
        data_graphs[key] = graph
    return data_graphs

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from typing import List


from database.db import get_db
from constants.const import DATA
from schemas.graph import GraphCreate, GraphResponse, GraphUpdate
from services.graph import (
    create_graph, read_graph, read_graphs,
    drop_graph
)

router = APIRouter()


@router.get('/{graph_id}')
async def get_img(graph_id: int, db: Session = Depends(get_db)) -> FileResponse:
    graph: GraphResponse | None = read_graph(graph_id, db)
    if graph is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f'graph id {graph_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(FileResponse(graph.image_url))}
    )


@router.get('/', response_model=List[GraphResponse])
async def get_graphs(db: Session = Depends(get_db)):
    graphs: List[GraphResponse] = read_graphs(db)
    if not graphs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'graphs not found: {graphs}'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(graphs)}
    )


@router.delete('/{graph_id}')
async def delete_graphs(approx_id: int, db: Session = Depends(get_db)):
    graph_dropped: bool = drop_graph(approx_id, db)
    if not graph_dropped:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'graph id {approx_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(graph_dropped)}
    )


# @router.post('/', response_model=GraphResponse)
# def upload_to_azure(blob_service_client, data):
#     blob_client = blob_service_client.get_blob_client(
#         container=CONTAINER_NAME, blob=BLOB_NAME
#     )
#     blob_client.upload_blob(data)


# router.mount("/images", StaticFiles(directory="backend/images"), name="images")

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from constants.const import DATA

from schemas.approx import ApproxCreate, ApproxResponse, ApproxUpdate
from schemas.constant import ConstantResponse
from schemas.graph import GraphResponse

from services.approx import (
    create_approx, read_approxs, read_approx,
    replace_approx, update_approx, remove_approx,
    create_graphs,
    read_graphs
)

router = APIRouter()


@router.post('/', response_model=ApproxResponse)
async def post_approx(approx: ApproxCreate, db: Session = Depends(get_db)):
    created_approx: ApproxResponse = create_approx(approx, db)
    if created_approx is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'approx_created title {approx.title} already exists'
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={DATA: jsonable_encoder(created_approx)}
    )


@router.get('/', response_model=List[ApproxResponse])
async def get_approxs(db: Session = Depends(get_db)) -> List[ApproxResponse]:
    approxs: List[ApproxResponse] = read_approxs(db)
    if not approxs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'approxs not found: {approxs}'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(approxs)}
    )


@router.get('/{approx_id}', response_model=ApproxResponse)
async def get_approx(approx_id: int, db: Session = Depends(get_db)) -> ApproxResponse:
    approx: ApproxResponse = read_approx(approx_id, db)
    if approx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'approx id {approx_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(approx)}
    )


@router.put('/{approx_id}', response_model=ApproxResponse)
async def put_approx(approx_id: int, approx: ApproxUpdate, db: Session = Depends(get_db)) -> ApproxResponse:
    replacer_approx: ApproxResponse = replace_approx(approx_id, approx, db)
    if replacer_approx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'approx id {approx_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(replacer_approx)}
    )


@router.patch('/{approx_id}', response_model=ApproxResponse)
async def patch_approx(approx_id: int, approx: ApproxUpdate, db: Session = Depends(get_db)) -> ApproxResponse:
    patcher_approx: ApproxResponse = update_approx(approx_id, approx, db)
    if patcher_approx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'approx id {approx_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(patcher_approx)}
    )


@router.delete('/{approx_id}')
async def delete_approx(approx_id: int, db: Session = Depends(get_db)) -> bool:
    existed_approx: bool = remove_approx(approx_id, db)
    status_code: int = status.HTTP_200_OK\
        if existed_approx else status.HTTP_404_NOT_FOUND
    return JSONResponse(
        status_code=status_code,
        content={DATA: existed_approx}
    )


@router.get('/{approx_id}/solve')
async def solve_approx(approx_id: int, db: Session = Depends(get_db)) -> int:
    # Generate all graphs from models Euler, RK4 & RK45.
    code = create_graphs(approx_id, db)
    if code >= status.HTTP_300_MULTIPLE_CHOICES:
        raise HTTPException(
            status_code=code,
            detail=f'approx id {approx_id} not found'
        )
    return JSONResponse(
        status_code=code,
        content={DATA: jsonable_encoder(code)}
    )


# @router.get('/{approx_id}/consts')
# async def get_consts(approx_id: int, db: Session = Depends(get_db)) -> List[ConstantResponse]:
#     consts: List[ConstantResponse] = read_consts(approx_id, db)
#     if not consts:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'consts not found: {consts}'
#         )
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={DATA: jsonable_encoder(consts)}
#     )


@router.get('/{approx_id}/graphs')
async def get_graphs(approx_id: int, db: Session = Depends(get_db)) -> List[GraphResponse]:
    graphs: List[GraphResponse] = read_graphs(approx_id, db)
    if not graphs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'graphs not found: {graphs}'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(graphs)}
    )

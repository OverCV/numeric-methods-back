from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from constants.const import DATA
from schemas.approx import ApproxCreate, ApproxRead, ApproxUpdate
from services.approx import (
    create_approx, read_approxs, read_approx,
    replace_approx, update_approx, remove_approx
)

router = APIRouter()


@router.post('/', response_model=ApproxRead)
async def post_approx(approx: ApproxCreate, db: Session = Depends(get_db)):
    created_approx: ApproxRead = create_approx(approx, db)
    if created_approx is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'approx_created title {approx.title} already exists'
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={DATA: jsonable_encoder(created_approx)}
    )


@router.get('/', response_model=List[ApproxRead])
async def get_approxs(db: Session = Depends(get_db)) -> List[ApproxRead]:
    approxs: List[ApproxRead] = read_approxs(db)
    if not approxs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'approxs not found: {approxs}'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(approxs)}
    )


@router.get('/{approx_id}', response_model=ApproxRead)
async def get_approx(approx_id: int, db: Session = Depends(get_db)) -> ApproxRead:
    approx: ApproxRead = read_approx(approx_id, db)
    if approx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'approx id {approx_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(approx)}
    )


@router.put('/{approx_id}', response_model=ApproxRead)
async def put_approx(approx_id: int, approx: ApproxUpdate, db: Session = Depends(get_db)) -> ApproxRead:
    replacer_approx: ApproxRead = replace_approx(approx_id, approx, db)
    if replacer_approx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'approx id {approx_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(replacer_approx)}
    )


@router.patch('/{approx_id}', response_model=ApproxRead)
async def patch_approx(approx_id: int, approx: ApproxUpdate, db: Session = Depends(get_db)) -> ApproxRead:
    patcher_approx: ApproxRead = update_approx(approx_id, approx, db)
    if patcher_approx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'approx id {approx_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(
            update_approx(approx_id, approx, db))}
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




# @router.get('/solve/{approx_id}', response_model=ApproxRead)
# async def solve_approx(approx_id: int, db: Session = Depends(get_db)) -> ApproxRead:
#     if not exist_approx_id(approx_id, db):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'approx id {approx_id} not found'
#         )
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content={ DATA: jsonable_encoder(calculate_approx( approx_id}, db))
#     )

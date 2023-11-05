from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from schemas.approx import ApproxCreate, ApproxRead, ApproxUpdate
# from services.approx import (
#     create_approx, read_approxs, read_approx, replace_approx,
#     update_approx, remove_approx, exist_approx_title, exist_approx_id,
#     calculate_approx
# )

router = APIRouter()


# @router.post('/', response_model=approxSchema)
# async def post_approx(approx: approxCreate, db: Session = Depends(get_db)):
#     let 
#     if exist_approx_title(approx.title, db):
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=f'approx title {approx.title} already exists'
#         )
#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content=jsonable_encoder(create_approx(approx, db))
#     )


# @router.get('/', response_model=List[approxSchema])
# async def get_approxs(db: Session = Depends(get_db)) -> List[approxSchema]:
#     approxs: List[approxSchema] = read_approxs(db)
#     if not approxs:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'approxs not found: {approxs}'
#         )
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=jsonable_encoder(approxs)
#     )


# @router.get('/{approx_id}', response_model=approxSchema)
# async def get_approx(approx_id: int, db: Session = Depends(get_db)) -> approxSchema:
#     if not exist_approx_id(approx_id, db):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'approx id {approx_id} not found'
#         )
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=jsonable_encoder(read_approx(approx_id, db))
#     )


# @router.put('/{approx_id}', response_model=approxSchema)
# async def put_approx(approx_id: int, approx: approxUpdate, db: Session = Depends(get_db)) -> approxSchema:
#     if not exist_approx_id(approx_id, db):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'approx id {approx_id} not found'
#         )
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=jsonable_encoder(replace_approx(approx_id, approx, db))
#     )


# @router.patch('/{approx_id}', response_model=approxSchema)
# async def patch_approx(approx_id: int, approx: approxUpdate, db: Session = Depends(get_db)) -> approxSchema:
#     if not exist_approx_id(approx_id, db):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'approx id {approx_id} not found'
#         )
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=jsonable_encoder(update_approx(approx_id, approx, db))
#     )


# @router.delete('/{approx_id}', response_model=approxSchema)
# async def delete_approx(approx_id: int, db: Session = Depends(get_db)) -> approxSchema:
#     if not exist_approx_id(approx_id, db):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'approx id {approx_id} not found'
#         )
#     return JSONResponse(
#         status_code=status.HTTP_202_ACCEPTED,
#         content=jsonable_encoder(remove_approx(approx_id, db))
#     )


# @router.get('/solve/{approx_id}', response_model=approxSchema)
# async def solve_approx(approx_id: int, db: Session = Depends(get_db)) -> approxSchema:
#     if not exist_approx_id(approx_id, db):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'approx id {approx_id} not found'
#         )
#     return JSONResponse(
#         status_code=status.HTTP_200_OK,
#         content=jsonable_encoder(calculate_approx(approx_id, db))
#     )

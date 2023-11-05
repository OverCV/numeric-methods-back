from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from schemas.euler import EulerCreate, EulerUpdate, EulerSchema
from services.euler import (
    create_euler, read_eulers, read_euler, replace_euler,
    update_euler, remove_euler, exist_euler_title, exist_euler_id,
    calculate_euler
)

router = APIRouter()


@router.post('/', response_model=EulerSchema)
async def post_euler(euler: EulerCreate, db: Session = Depends(get_db)):
    if exist_euler_title(euler.title, db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Euler title {euler.title} already exists'
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder(create_euler(euler, db))
    )


@router.get('/', response_model=List[EulerSchema])
async def get_eulers(db: Session = Depends(get_db)) -> List[EulerSchema]:
    eulers: List[EulerSchema] = read_eulers(db)
    if not eulers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Eulers not found: {eulers}'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(eulers)
    )


@router.get('/{euler_id}', response_model=EulerSchema)
async def get_euler(euler_id: int, db: Session = Depends(get_db)) -> EulerSchema:
    if not exist_euler_id(euler_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Euler id {euler_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(read_euler(euler_id, db))
    )


@router.put('/{euler_id}', response_model=EulerSchema)
async def put_euler(euler_id: int, euler: EulerUpdate, db: Session = Depends(get_db)) -> EulerSchema:
    if not exist_euler_id(euler_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Euler id {euler_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(replace_euler(euler_id, euler, db))
    )


@router.patch('/{euler_id}', response_model=EulerSchema)
async def patch_euler(euler_id: int, euler: EulerUpdate, db: Session = Depends(get_db)) -> EulerSchema:
    if not exist_euler_id(euler_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Euler id {euler_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(update_euler(euler_id, euler, db))
    )


@router.delete('/{euler_id}', response_model=EulerSchema)
async def delete_euler(euler_id: int, db: Session = Depends(get_db)) -> EulerSchema:
    if not exist_euler_id(euler_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Euler id {euler_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content=jsonable_encoder(remove_euler(euler_id, db))
    )


@router.get('/solve/{euler_id}', response_model=EulerSchema)
async def solve_euler(euler_id: int, db: Session = Depends(get_db)) -> EulerSchema:
    if not exist_euler_id(euler_id, db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Euler id {euler_id} not found'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(calculate_euler(euler_id, db))
    )
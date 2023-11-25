from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List

from database.db import get_db
from constants.const import DATA
from schemas.constant import ConstantCreate, ConstantResponse, ConstantUpdate
from services.const import (
    create_const, read_consts, read_const, update_const,
    remove_const, read_by_approx
)

router = APIRouter()


@router.get('/all', response_model=List[ConstantResponse])
async def get_consts(db: Session = Depends(get_db)) -> List[ConstantResponse]:
    consts: List[ConstantResponse] = read_consts(db)
    if not consts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'consts not found: {consts}'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(consts)}
    )


@router.get('/by_approx/{approx_id}', response_model=List[ConstantResponse])
async def get_by_approx(approx_id: int, db: Session = Depends(get_db)) -> List[ConstantResponse]:
    consts: List[ConstantResponse] = read_by_approx(approx_id, db)
    if not consts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'consts not found: {consts}'
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={DATA: jsonable_encoder(consts)}
    )


@router.post('/post/{approx_id}', response_model=ConstantResponse)
async def post_const(approx_id: int, const: ConstantCreate, db: Session = Depends(get_db)):
    created_const, code = create_const(approx_id, const, db)
    if code >= status.HTTP_300_MULTIPLE_CHOICES:
        raise HTTPException(
            status_code=code,
            detail=f'const {const.name} has an {code} code.'
        )
    return JSONResponse(
        status_code=code,
        content={DATA: jsonable_encoder(created_const)}
    )


@router.get('/by_id/{const_id}')
async def get_const(const_id: int, db: Session = Depends(get_db)) -> ConstantResponse:
    const, code = read_const(const_id, db)
    if code >= status.HTTP_300_MULTIPLE_CHOICES:
        raise HTTPException(
            status_code=code,
            detail=f'const id {const_id} has an {code} code.'
        )
    return JSONResponse(
        status_code=code,
        content={DATA: jsonable_encoder(const)}
    )


@router.put('/put/{const_id}', response_model=ConstantResponse)
async def put_const(const_id: int, const: ConstantUpdate, db: Session = Depends(get_db)):
    updated_const, code = update_const(const_id, const, db)
    if code >= status.HTTP_300_MULTIPLE_CHOICES:
        raise HTTPException(
            status_code=code,
            detail=f'const id {const_id} has an {code} code.'
        )
    return JSONResponse(
        status_code=code,
        content={DATA: jsonable_encoder(updated_const)}
    )


@router.delete('/delete/{const_id}', response_model=ConstantResponse)
async def delete_const(const_id: int, db: Session = Depends(get_db)):
    deleted_const, code = remove_const(const_id, db)
    if code >= status.HTTP_300_MULTIPLE_CHOICES:
        raise HTTPException(
            status_code=code,
            detail=f'const id {const_id} has an {code} code.'
        )
    return JSONResponse(
        status_code=code,
        content={DATA: jsonable_encoder(code)}
    )

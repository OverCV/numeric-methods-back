import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from middlewares.error import ErrorHandler

from constants.const import NG_LOCALE_URL, IMG_DIR
from database.db import Base, engine
from routers import (
    approx, graph, const
)


Base.metadata.create_all(bind=engine)
app: FastAPI = FastAPI()

app.title = 'Numeric methods | Models'
app.version = '1.0.0'
app.mount(
    f'/{IMG_DIR}',
    StaticFiles(directory=f'{IMG_DIR}'), name=IMG_DIR
)

# Adicion de middlewares
app.add_middleware(ErrorHandler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[NG_LOCALE_URL], allow_credentials=True,
    allow_methods=['*'], allow_headers=['*']
)

app.include_router(approx.router, tags=['Approxs'], prefix='/approx')
app.include_router(graph.router, tags=['Graphs'], prefix='/graph')
app.include_router(const.router, tags=['Consts'], prefix='/const')


@app.get('/')
async def root():
    return {'message': 'Hello math!'}

if __name__ == '__main__':
    kwargs = {'host': 'localhost', 'port': 8300}
    kwargs.update({'debug': True, 'reload': True})
    uvicorn.run('main:app', **kwargs, reload=True)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import Base, engine
from routers import approx


Base.metadata.create_all(bind=engine)
app: FastAPI = FastAPI()

app.title = 'Numeric methods | Models'
app.version = '1.0.0'

origins = [
    'http://localhost:4200',
]

app.include_router(approx.router, tags=['Approx'], prefix='/approx')


app.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


@app.get('/')
async def root():
    return {'message': 'Hello math!'}

if __name__ == '__main__':
    kwargs = {'host': 'localhost', 'port': 8000}
    kwargs.update({'debug': True, 'reload': True})
    uvicorn.run('main:app', **kwargs, reload=True)

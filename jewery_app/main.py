from fastapi import FastAPI
import uvicorn
from models.gem_models import *
from db import engine
import gem_repository

app = FastAPI()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get('/gems')
def gems():
    gems = gem_repository.select_all_gems()
    return ({'Gems': gems})

@app.get('/gems/{id}')
def gem(id: int):
    gems = gem_repository.select_gem(id)
    return ({'Gems': gems})


if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost',port=8000, reload=True)
    create_db_and_tables()
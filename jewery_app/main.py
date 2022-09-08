from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import uvicorn
from models.gem_models import *
from db import engine
import gem_repository
from sqlmodel import Session
from populate import calculate_gem_price
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED


app = FastAPI()
session = Session(bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get('/gems')
def gems():
    gems = gem_repository.select_all_gems()
    return ({'Gems': gems})

@app.get('/gem/{id}', response_model=Gem)
def gem(id: int):
    gem_found = session.get(Gem, id)
    if not gem_found:
        return JSONResponse('Gem does not Exist!', status_code=HTTP_404_NOT_FOUND)
    return (gem_found)


@app.post('/gems',  response_model=Gem)
def create_gem(gem_pr:GemProperties, gem:Gem):
    gem_properties = GemProperties(size=gem_pr.size, clarity=gem_pr.clarity,
                                   color=gem_pr.color)
    session.add(gem_properties)
    session.commit()
    gem_ = Gem(price=gem.price, available=gem.available, gem_properties=gem_properties,
               gem_properties_id=gem_properties.id,gem_type=gem.gem_type)
    price = calculate_gem_price(gem, gem_pr)
    gem_.price = price
    session.add(gem_)
    session.commit()
    return (gem_)

@app.put('/gems/{id}', response_model=Gem)
def update_gem(id:int, gem:Gem):
    gem_found = session.get(Gem,id)
    update_item_encoded = jsonable_encoder(gem)
    update_item_encoded.pop('id', None)
    update_item_encoded.pop('gem_properties_id', None)
    for key, value in update_item_encoded.items():
        gem_found.__setattr__(key,value)
    session.commit()
    return (gem_found)

@app.patch('/gems/{id}', response_model=Gem)
def patch_gem(id:int, gem:GemPatch):
    gem_found = session.get(Gem,id)
    update_item_encoded = gem.dict(exclude_unset=True)
    for key, value in update_item_encoded.items():
        gem_found.__setattr__(key,value)
    session.commit()
    return (gem_found)

@app.delete('/gems/{id}')
def delete_gem(id:int):
    gem_found = session.get(Gem, id)
    if not gem_found:
        return (JSONResponse('Gem does not Exist!', status_code=HTTP_404_NOT_FOUND))
    session.delete(gem_found)
    session.commit()





if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost',port=8000, reload=True)
    create_db_and_tables()
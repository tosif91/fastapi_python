from typing import List 
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
    return "Hello world"


@app.get('/items/123')
async def getItem():
    return {"param":False}


@app.get('/items/{item_id}')
async def getItems(item_id : int):
    return {'item_id':item_id,"param":True}


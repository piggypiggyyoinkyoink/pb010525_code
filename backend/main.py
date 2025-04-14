from fastapi import FastAPI

app = FastAPI()
itemsDb = [{"itemName": "Skibidi"}, {"itemName":"Toilet"}, {"itemName":"Sigma"}]

@app.get("/")
async def root():
    return {"message":"Hello World"}

@app.get("/items/{itemId}")
async def get_item(itemId:int): #type annotations automagically convert things to the correct type
    return {"itemId":itemId}

@app.get("/items/") # skip and limit are passed as query params here, e.g. http://127.0.0.1:8000/items/?skip=0&limit=10
async def readItem(skip:int=0, limit:int=10):
    return itemsDb[skip:skip+limit]
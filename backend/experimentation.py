from fastapi import FastAPI, status
from pydantic import BaseModel

class Item(BaseModel): #this is a data model, with fields and their types (and optional-ness) defined.
    name:str
    desc:str|None=None
    price:float
    tax:float|None=None

app = FastAPI()
itemsDb = [{"itemName": "itemOne"}, {"itemName":"itemTwo"}, {"itemName":"itemThree"}]

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message":"Hello World"}

@app.get("/items/{itemId}", status_code=status.HTTP_200_OK)
async def get_item(itemId:int): #type annotations automagically convert things to the correct type
    return {"itemId":itemId}

@app.get("/items/", status_code=status.HTTP_200_OK) # skip and limit are passed as query params here, e.g. http://127.0.0.1:8000/items/?skip=0&limit=10
async def readItem(skip:int=0, limit:int=10, q: str|None=None): # q is an optional query param, defaults to None if does not exist here. The | specifies that it can be of type str or None (as None is not a string)
    if q:
        return q
    else:
        return itemsDb[skip:skip+limit]
    
@app.get("/areyouhuman/", status_code=status.HTTP_200_OK)
async def getAnswer(answer:bool = False): #Boolean query params accept values true, 1, yes and on for True, and anything else for False
    if answer:
        return "Hello human"
    else:
        return "beep boop"
    
@app.get("/answermeorelse", status_code=status.HTTP_200_OK)
async def greeting(ans:str): #since no default value specified, this will throw an error if no value of ans is provided as a query param
    return "Good Morning."

@app.post("/items/", status_code=status.HTTP_201_CREATED) #http codes are returned if the code executes successfully, otherwise 40x status codes are automatically returned instead
async def createItem(item:Item): #add the Item class as the type of the parameter -> these are request body parameters
    itemDict = item.dict()
    if item.tax is not None:
        praceWithTax = item.price + item.tax
        itemDict.update({"priceWithTax":praceWithTax})
    return itemDict

#note: body, path and query parameters can be mix n matched and fastapi is awesome and can just figure out which is which :)
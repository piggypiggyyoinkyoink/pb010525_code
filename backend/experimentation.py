from fastapi import FastAPI, status, Query, Path, Body
from pydantic import BaseModel, Field
from typing import Annotated

class Item(BaseModel): #this is a data model, with fields and their types (and optional-ness) defined.
    name:str
    desc:str|None= Field(default=None, titile = "Description of item", max_length=100) #can use Field to define validation restrictions on model data
    price:float = Field(gt=0, description = "price must be > 0")
    tax:float|None=None

class User(BaseModel):
    username:str
    fullName: str|None=None

app = FastAPI()
itemsDb = [{"name": "itemOne", "price":7.0}, {"name":"itemTwo", "price":5.30}, {"name":"itemThree", "desc":"Very useful item", "price":2.50}]

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message":"Hello World"}

@app.get("/items/{itemId}", status_code=status.HTTP_200_OK)
async def get_item(itemId:Annotated[int, Path(title="The ID of the item to get", ge=1)]): #type annotations automagically convert things to the correct type
    #adding Annotated above with a Path() (as it is a path parameter). Title here defines some metadata for the parameter.
    #ge = greater or equal to -> use gt, le, lt for >, <= and <. This can be used for int and float params.
    return {"itemId":itemId}

@app.get("/items/", status_code=status.HTTP_200_OK, response_model=list[Item]) # skip and limit are passed as query params here, e.g. http://127.0.0.1:8000/items/?skip=0&limit=10. Response model provides validation for the response data, and makes sure it fits the Item model structure, filtering out anything unwanted.
async def readItem(skip:int=0, limit:int=10, q: Annotated[int|None, Query()]=None): # q is an optional query param, defaults to None if does not exist here. The | specifies that it can be of type str or None (as None is not a string)
    # use of Annotated above allows us to define more validation restrictions defined using a fastapi Query() function (as it is a query param). Parameter is still optional as it still has a default value. Queries can also accept regex (oh no)
    if q:
        return [itemsDb[q-1]]
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
async def createItem(item:Item) -> Item: #add the Item class as the type of the parameter -> these are request body parameters. the '-> Item' specifies the type of the returned data.
    return item

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    item: Item,
    user: User,
    priority: Annotated[int, Body()]
): #fastapi automatically converts a JSON request body with keys "user" and "item" into Item and User objects. Use Body() for single values passed into the body
    results = {"item_id": item_id, "item":item, "user":user}
    
    return results
#note: body, path and query parameters can be mix n matched and fastapi is awesome and can just figure out which is which :)


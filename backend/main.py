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
async def readItem(skip:int=0, limit:int=10, q: str|None=None): # q is an optional query param, defaults to None if does not exist here. The | specifies that it can be of type str or None (as None is not a string)
    if q:
        return q
    else:
        return itemsDb[skip:skip+limit]
    
@app.get("/areyouhuman/")
async def getAnswer(answer:bool = False): #Boolean query params accept values true, 1, yes and on for True, and anything else for False
    if answer:
        return "Hello human"
    else:
        return "beep boop"
    
@app.get("/answermeorelse")
async def greeting(ans:str): #since no default value specified, this will throw an error if no value of ans is provided as a query param
    return "Good Morning."
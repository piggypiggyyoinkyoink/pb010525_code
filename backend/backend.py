from fastapi import FastAPI, HTTPException, status, Depends, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Any
from contextlib import asynccontextmanager
from hashlib import sha3_256
import jwt
from jwt.exceptions import ExpiredSignatureError
from cryptography.hazmat.primitives import serialization

private_key = open('.ssh/id_rsa', 'r').read()
PRIVATE_KEY = serialization.load_ssh_private_key(private_key.encode(), password=b'')
public_key = open('.ssh/id_rsa.pub', 'r').read()
PUBLIC_KEY = serialization.load_ssh_public_key(public_key.encode())

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "hashed_password": "f5a5207a8729b1f709cb710311751eb2fc8acad5a1fb8ac991b736e69b6529a3",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "first_name": "Alice",
        "last_name": "Inwonderland",
        "email": "alice@example.com",
        "hashed_password": "74efee2654fbc20723cb7eb381e464be96319c23064a4ffce86a5de8470dd863",
        "disabled": True,
    },
}


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Hello")
    global APPLES
    APPLES = 7
    print(sha3_256(bytes("secret2", "utf-8")).hexdigest())
    yield
    print("Goodbye")


app = FastAPI(lifespan=lifespan)

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost:5173",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class User(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str



def hash_password(password: str):
    return sha3_256(bytes(password, "utf-8")).hexdigest()

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def hgg(db, username:str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)
    
def decode_token(token):
    try:
        payload = jwt.decode(jwt=token, key=PUBLIC_KEY, algorithms=['RS256', ])
        print(payload)
        return get_user(fake_users_db, payload["sub"])
    except ExpiredSignatureError:
        raise ExpiredSignatureError


async def get_current_user(token: Annotated[str, Depends(oauth2Scheme)]):
    user = decode_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return user
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message":"Hello World"}



@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    print(user_dict)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    jwt_payload = {"sub": user.username}
    
    token = jwt.encode(payload=jwt_payload, key=PRIVATE_KEY, algorithm="RS256")
    print(token)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
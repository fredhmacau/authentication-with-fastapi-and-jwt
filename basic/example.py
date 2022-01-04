from fastapi import FastAPI
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from schema import User


api = FastAPI()


oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


@api.post("/token")
async def token_authorization(user: User):
    return {"access_token": user.username + "token"}


@api.get("/items")
async def items(token: str = Depends(oauth_scheme)):
    return {"token": token}

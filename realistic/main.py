from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from schema_type import Users
from schema_db import db
from bcrypt import hashpw, gensalt
from uvicorn import run
from verify_pw import Verificator
from jose import jwt

api = FastAPI()
verificator = Verificator()
JWT_SECRET = "62af11164f7b94e9ad42367c6c2b8ec5b63d18f64ab90572630bd66d0b00f406"
oauth_schema = OAuth2PasswordBearer(tokenUrl="token")


@api.on_event("startup")
async def startup_event():
    await db.connect()


@api.get("/", status_code=status.HTTP_202_ACCEPTED)
async def index():
    return {"create_by": "Fredh Macau"}


@api.post("/token")
async def create_token(user: Users):
    user_value = await verificator.authenticate_user(user.username, user.password)
    if not user_value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and password",
        )
    else:
        user_obj = {
            "id": user_value.id,
            "username": user.username,
            "password": user.password,
        }
        token = jwt.encode(user_obj, JWT_SECRET)
        return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token: str = Depends(oauth_schema)):
    try:
        payload = jwt.decode(token, JWT_SECRET)
        user = await verificator.select_user(payload.get("id"))
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and password",
        )


@api.post("/users", status_code=status.HTTP_201_CREATED, tags=["user"])
async def create_user(user: Users):
    query = "INSERT INTO users(username,password_hash) values(:username,:password_hash)"
    values = {
        "username": str(user.username).strip().lower(),
        "password_hash": hashpw(user.password.encode("utf-8"), gensalt()),
    }
    await db.execute(query, values=values)

    return {"message": "user created"}


@api.get("/users/me", tags=["user"])
async def current_user(user: Users = Depends(get_current_user)):
    return user


@api.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()


if __name__ == "__main__":
    run(api, host="0.0.0.0", port=8080)

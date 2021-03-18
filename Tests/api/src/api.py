import os
from typing import List
from enum import Enum
import uvicorn
import httpx
import requests
import databases
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, BaseSettings

try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv()


class UserFactory(BaseModel):
    name: str


class User(BaseModel):
    id: int
    name: str


class SexEnum(str, Enum):
    male = 'm'
    female = 'f'


class UserInfo(BaseModel):
    sex: SexEnum


API_URL = ''


class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8888
    postgresql_host: str
    postgresql_port: int
    postgresql_dbname: str
    postgresql_user: str
    postgresql_password: str

    @property
    def database_url(self):
        return (
            f"postgresql://{self.postgresql_user}:{self.postgresql_password}"
            + f"@{self.postgresql_host}:{self.postgresql_port}/{self.postgresql_dbname}"
        )


settings = Settings()

db = databases.Database(settings.database_url)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.connect()

    # query = """CREATE TABLE my_user (id serial, name text)"""
    # await db.execute(query=query)


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/users")
async def get_users() -> List[User]:
    query = "SELECT * FROM my_user"
    return await db.fetch_all(query=query)


@app.get("/users/{id}")
async def get_user_by_id(id: int) -> User:
    query = "SELECT * FROM my_user WHERE id=:id"
    row = await db.fetch_one(query, {"id": id})

    if row is None:
        raise HTTPException(status_code=404, detail="User not found")

    return row


@app.post("/users")
async def create_user(user_data: UserFactory) -> User:
    query = "INSERT INTO my_user (name) VALUES (:name) RETURNING id as id, name as name"
    return await db.fetch_one(query=query, values=user_data.dict())


@app.get("/users/{id}/info")
async def get_users_info(id: int) -> UserInfo:
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        return response.json()


@app.get("/users/{id}/info/other")
def get_users_info_other(id: int) -> UserInfo:
    response = requests.get(API_URL)
    return response.json()


if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port)

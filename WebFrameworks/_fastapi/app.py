import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    first_name: str
    last_name: str


def get_users():
    """Типа обращение к бд"""
    return [User(first_name='Vitaliy', last_name='Afanasyev')]


@app.get("/")
def users():
    return get_users()


if __name__ == "__main__":
    uvicorn.run(app)

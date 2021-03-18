"""
Popular aio frameworks and some info: https://github.com/timofurrer/awesome-asyncio
"""


import time
from typing import List
import asyncio
import uvicorn
# import motor.motor_asyncio
from fastapi import FastAPI
from pydantic import BaseModel, BaseSettings
from databases import Database
from aiokafka import AIOKafkaProducer
import aioredis

try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv()


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    MONGO_HOST: str
    MONGO_PORT: int
    MONGO_USER: str
    MONGO_PASSWORD: str
    KAFKA_HOST: str
    KAFKA_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int


class Record(BaseModel):
    first: str
    last: str


app = FastAPI()

settings = Settings()

postgres_db = Database(f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}')

redis = None

producer = None

data = [
    {"first": "Vitaliy", "last": "Afanasyev"},
    {"first": "Dmitry", "last": "Avdeev"},
    {"first": "Evgeny", "last": "Panteleev"},
]


@app.on_event("startup")
async def startup():
    global producer, redis
    producer = AIOKafkaProducer(bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}')
    redis = await aioredis.create_redis_pool(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    await producer.start()
    await postgres_db.connect()

    query = """CREATE TABLE test (first text, last text)"""
    await postgres_db.execute(query=query)

    query = "INSERT INTO test(first, last) VALUES (:first, :last)"
    await postgres_db.execute_many(query=query, values=data)

    # mongo_db.insert_many(data)


@app.on_event("shutdown")
async def shutdown():
    await postgres_db.disconnect()
    await producer.stop()
    redis.close()
    await redis.wait_closed()
    # mongo_db.close()


@app.get("/synchronous")
async def synchronous():
    time.sleep(2)
    return {"Hello": "World"}


@app.get("/asynchronous")
async def asynchronous():
    await asyncio.sleep(2)
    return {"Hello": "World"}


@app.get("/postgre")
async def postgre() -> List[Record]:
    query = "SELECT * FROM test"
    rows = await postgres_db.fetch_all(query=query)
    return rows 


@app.get("/kafka_producer")
async def kafka_producer() -> List[Record]: 
    """
    async def send_and_wait(
        self, topic, value=None, key=None, partition=None,
        timestamp_ms=None, headers=None
    ):
        future = await self.send(
            topic, value, key, partition, timestamp_ms, headers)
        return (await future)
    """
    return await producer.send_and_wait("my_topic", b"Super message")


@app.get("/redis_set")
async def redis_set(key: str, value: str):
    await redis.set(key, value)


@app.get("/redis_get")
async def redis_get(key: str) -> str:
    return await redis.get(key)


if __name__ == '__main__':
    uvicorn.run(app)

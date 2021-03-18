from aiokafka import AIOKafkaConsumer
import asyncio
from pydantic import BaseSettings


try:
    from dotenv import load_dotenv
except ImportError:
    pass
else:
    load_dotenv()


class Settings(BaseSettings):
    KAFKA_HOST: str
    KAFKA_PORT: int


settings = Settings()


async def consume():
    consumer = AIOKafkaConsumer(
        'my_topic',
        bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
        group_id="my-group"
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


if __name__ == '__main__':
    asyncio.run(consume())
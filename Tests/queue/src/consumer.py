import json
from confluent_kafka import Consumer, Producer
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
    TOPIC_INPUT: str
    TOPIC_OUTPUT: str
    GROUP_ID: str
    OFFSET: str


settings = Settings()


producer = Producer({
    "bootstrap.servers": f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
})


consumer = Consumer(
    {
        "bootstrap.servers": f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
        "enable.auto.commit": True,
        "group.id": settings.GROUP_ID,
        "auto.offset.reset": settings.OFFSET,
    },
)
consumer.subscribe([settings.TOPIC_INPUT])


def receive_from_kafka():
    while True:
        message = consumer.poll(1)
        if message is not None:
            if message.error():
                print("Message is shit")
            else:
                return json.loads(message.value())


def send_to_kafka(message):
    producer.produce(value=json.dumps(message), topic=settings.TOPIC_OUTPUT)
    producer.flush()


def main():
    while True:
        payload = receive_from_kafka()
        send_to_kafka(payload)


if __name__ == "__main__":
    main()

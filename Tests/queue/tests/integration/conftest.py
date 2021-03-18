# python -m pytest tests/integration/
import sys
sys.path.append('./src')

import pytest

from confluent_kafka import Consumer, Producer
from consumer import settings


@pytest.fixture()
def producer():
    return Producer({
        "bootstrap.servers": f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
    })


@pytest.fixture()
def consumer():
    c = Consumer(
        {
            "bootstrap.servers": f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
            "enable.auto.commit": True,
            "group.id": settings.GROUP_ID + "TEST",
            "auto.offset.reset": settings.OFFSET,
        },
    )
    c.subscribe([settings.TOPIC_OUTPUT])
    return c
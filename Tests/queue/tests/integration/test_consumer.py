
import json
from consumer import settings


def test_consumer(producer, consumer):
    expected_message = {"test": "It's test"}

    producer.produce(value=json.dumps(expected_message), topic=settings.TOPIC_INPUT)
    producer.flush()

    message = consumer.poll(5)

    assert message is not None
    assert {} == json.loads(message.value())  # special fo fail

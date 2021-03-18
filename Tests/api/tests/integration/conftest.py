# python -m pytest tests/integration/
import sys
sys.path.append('./src')

import requests

import pytest

from api import app, settings

from fastapi.testclient import TestClient
import psycopg2


@pytest.fixture(scope="function")
def db():
    connection = psycopg2.connect(settings.database_url)

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("DROP TABLE my_user")
            except:
                pass
            cursor.execute("CREATE TABLE my_user (id serial, name text)")

    with connection:
        with connection.cursor() as cursor:
            yield cursor

    connection.close()


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client

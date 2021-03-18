import mock
import httpx
import requests
import api


def mock_get_api(status_code, return_value):
    def get(url, *args, **kwargs):
        if url == api.API_URL:
            response = mock.Mock()
            response.status_code = status_code
            response.json.return_value = return_value
            return response
        else:
            return requests.get(url, *args, **kwargs)

    return get


def test_get_users(client, db):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []

    db.execute("INSERT INTO my_user (name) VALUES (%s)", ("Vitaly",))
    db.connection.commit()
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Vitaly"}]

    db.execute("INSERT INTO my_user (name) VALUES (%s)", ("Somebody",))
    db.connection.commit()
    ans = [{"id": 1, "name": "Vitaly"}, {"id": 2, "name": "Somebody"}]
    response = client.get("/users")
    assert response.status_code == 200

    #1
    assert sorted(response.json(), key=lambda x: x['id']) == sorted(ans, key=lambda x: x['id'])

    #2
    assert len(response.json()) == len(ans)
    assert {(x['id'], x['name']) for x in response.json()} == {(x['id'], x['name']) for x in ans}


def test_only_for_test(client, db):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_get_user_by_id(client, db):
    response = client.get("/users/9999999")
    assert response.status_code == 404

    db.execute("INSERT INTO my_user (name) VALUES (%s)", ("Vitaly",))
    db.connection.commit()
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Vitaly"}

    response = client.get("/users/2")
    assert response.status_code == 404


def test_create_user(client, db):
    db.execute("SELECT * FROM my_user")
    rows = db.fetchall()
    assert rows == []

    response = client.post("/users", json={"name": "Vitaly"})
    print(response.text)
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Vitaly"}

    db.execute("SELECT * FROM my_user")
    rows = db.fetchall()
    assert rows == [(1, "Vitaly")]

    response = client.post("/users", json={"name": "Somebody"})
    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "Somebody"}

    db.execute("SELECT * FROM my_user")
    rows = db.fetchall()
    ans = [(1, "Vitaly"), (2, "Somebody")]

    #1
    assert sorted(rows) == sorted(ans)

    #2
    assert len(rows) == len(ans)
    assert set(rows) == set(ans)


@mock.patch.object(httpx, 'AsyncClient')
def test_get_users_info(_, client):
    httpx.AsyncClient.return_value.__aenter__.return_value = mock.AsyncMock()
    httpx.AsyncClient.return_value.__aenter__.return_value.get.return_value = mock.Mock()
    httpx.AsyncClient.return_value.__aenter__.return_value.get.return_value.json.return_value = {"sex": "m"}
    response = client.get("/users/1/info")
    assert response.status_code == 200
    assert response.json() == {"sex": "m"}


def test_get_users_info_other(client):
    with mock.patch('requests.get', side_effect=mock_get_api(200, {"sex": "f"})):
        response = client.get("/users/1/info/other")
        assert response.status_code == 200
        assert response.json() == {"sex": "f"}

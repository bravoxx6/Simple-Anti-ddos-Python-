import time
from conftest import reset_redis
def test_normal_request(client):
    response = client.get("/")
    assert response.status_code == 200


def test_rate_limit_trigger(client):
    # Превышаем лимит
    for _ in range(35):
        response = client.get("/")

    assert response.status_code == 429 or response.status_code == 403


def test_block_after_limit(client):
    for _ in range(40):
        client.get("/")

    blocked = client.get("/")
    assert blocked.status_code == 403


def test_different_user_agents(client):
    headers1 = {"User-Agent": "TestAgent1"}
    headers2 = {"User-Agent": "TestAgent2"}

    for _ in range(20):
        r1 = client.get("/", headers=headers1, environ_base={"REMOTE_ADDR": "127.0.0.1"})
        reset_redis()
        r2 = client.get("/", headers=headers2, environ_base={"REMOTE_ADDR": "127.0.0.2"})

    assert r1.status_code == 200
    assert r2.status_code == 200


def test_unblock_after_ttl(client):
    for _ in range(40):
        client.get("/")

    time.sleep(3)  # если BLOCK_TIME уменьшен для тестов

    response = client.get("/")
    assert response.status_code in (200, 429)
    
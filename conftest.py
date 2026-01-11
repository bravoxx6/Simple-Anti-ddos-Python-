import pytest
from app import app
import redis
from config import REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def reset_redis():
    r.flushdb()  # CLEAR FOR TEST PURPOSES ONLY

@pytest.fixture(autouse=True)
def clear_redis():
    r.flushdb()
    yield
    r.flushdb()
    
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


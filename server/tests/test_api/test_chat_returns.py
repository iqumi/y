import pytest
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient
from starlette.websockets import WebSocket
from database import Cassandra
from main import app


client = TestClient(app)


def test_read_main():
    response = client.post("/username", params={"username": "@max"})
    assert response.status_code == 200
    assert response.json() == True

'''
def test_chat_returns(private_chat):
    client = TestClient(app)
    user_id = {"user_id": private_chat.user_id}
    with client.websocket_connect("/ws", params=user_id) as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
'''

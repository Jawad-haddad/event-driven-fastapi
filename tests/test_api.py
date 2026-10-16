import pytest
from fastapi.testclient import TestClient

from app.container import Container
from app.main import app, get_container


@pytest.fixture
def container():
    fresh = Container()
    app.dependency_overrides[get_container] = lambda: fresh
    yield fresh
    app.dependency_overrides.clear()


@pytest.fixture
def client(container):
    return TestClient(app)


PAYLOAD = {"name": "Concert", "attendee_email": "a@b.com", "attendee_phone": "+962700000000"}


def test_creating_an_event_notifies_all_channels_and_reserves_a_ticket(client, container):
    response = client.post("/events", json=PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["ticket"].startswith("TICKET-")
    assert [len(c.sent) for c in container.channels] == [1, 1, 1]


def test_get_event_returns_the_created_event(client):
    event_id = client.post("/events", json=PAYLOAD).json()["event_id"]

    response = client.get(f"/events/{event_id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Concert"


def test_get_unknown_event_returns_404(client):
    assert client.get("/events/missing").status_code == 404


def test_missing_fields_are_rejected(client):
    assert client.post("/events", json={"name": "x"}).status_code == 422

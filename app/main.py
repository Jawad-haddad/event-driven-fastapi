from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from app.container import Container
from app.events import EventCreated

app = FastAPI(title="Event-Driven Demo")
container = Container()


def get_container() -> Container:
    return container


class CreateEventRequest(BaseModel):
    name: str
    attendee_email: str
    attendee_phone: str


@app.post("/events", status_code=201)
def create_event(body: CreateEventRequest, c: Container = Depends(get_container)):
    event = EventCreated.new(body.name, body.attendee_email, body.attendee_phone)
    c.events[event.event_id] = event
    c.publisher.publish(event)
    return {
        "event_id": event.event_id,
        "name": event.name,
        "ticket": c.ticket_service.reservations[event.event_id],
    }


@app.get("/events/{event_id}")
def get_event(event_id: str, c: Container = Depends(get_container)):
    event = c.events.get(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return {
        "event_id": event.event_id,
        "name": event.name,
        "ticket": c.ticket_service.reservations.get(event_id),
    }

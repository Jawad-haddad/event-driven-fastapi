from typing import Dict

from app.events import EventCreated
from app.publisher import Subscriber


class TicketService(Subscriber):

    def __init__(self) -> None:
        self.reservations: Dict[str, str] = {}

    def handle(self, event: EventCreated) -> None:
        self.reservations.setdefault(event.event_id, f"TICKET-{event.event_id[:8]}")

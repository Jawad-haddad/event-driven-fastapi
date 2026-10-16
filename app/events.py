from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class EventCreated:

    event_id: str
    name: str
    attendee_email: str
    attendee_phone: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def new(cls, name: str, attendee_email: str, attendee_phone: str) -> "EventCreated":
        return cls(str(uuid4()), name, attendee_email, attendee_phone)

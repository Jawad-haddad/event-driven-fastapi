from abc import ABC, abstractmethod
from typing import List

from app.events import EventCreated


class NotificationChannel(ABC):

    name: str

    def __init__(self) -> None:
        self.sent: List[str] = []

    @abstractmethod
    def recipient(self, event: EventCreated) -> str: ...

    def send(self, event: EventCreated) -> str:
        message = f"[{self.name}] to {self.recipient(event)}: '{event.name}' was created"
        self.sent.append(message)
        print(message)
        return message


class EmailChannel(NotificationChannel):
    name = "email"

    def recipient(self, event: EventCreated) -> str:
        return event.attendee_email


class SmsChannel(NotificationChannel):
    name = "sms"

    def recipient(self, event: EventCreated) -> str:
        return event.attendee_phone


class WhatsAppChannel(NotificationChannel):
    name = "whatsapp"

    def recipient(self, event: EventCreated) -> str:
        return event.attendee_phone

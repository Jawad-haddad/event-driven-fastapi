from typing import Dict

from app.events import EventCreated
from app.notifications.channels import EmailChannel, SmsChannel, WhatsAppChannel
from app.publisher import EventPublisher
from app.subscribers.notification_service import NotificationService
from app.subscribers.ticket_service import TicketService


class Container:
    def __init__(self) -> None:
        self.events: Dict[str, EventCreated] = {}
        self.channels = [EmailChannel(), SmsChannel(), WhatsAppChannel()]
        self.notification_service = NotificationService(self.channels)
        self.ticket_service = TicketService()

        self.publisher = EventPublisher()
        self.publisher.subscribe(self.notification_service)
        self.publisher.subscribe(self.ticket_service)

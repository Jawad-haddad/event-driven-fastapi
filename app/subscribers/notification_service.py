from typing import List

from app.events import EventCreated
from app.notifications.channels import NotificationChannel
from app.publisher import Subscriber


class NotificationService(Subscriber):

    def __init__(self, channels: List[NotificationChannel]) -> None:
        self.channels = channels

    def handle(self, event: EventCreated) -> None:
        for channel in self.channels:
            channel.send(event)

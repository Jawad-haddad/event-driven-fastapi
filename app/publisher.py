from abc import ABC, abstractmethod
from typing import List

from app.events import EventCreated


class Subscriber(ABC):

    @abstractmethod
    def handle(self, event: EventCreated) -> None: ...


class EventPublisher:

    def __init__(self) -> None:
        self._subscribers: List[Subscriber] = []

    def subscribe(self, subscriber: Subscriber) -> None:
        self._subscribers.append(subscriber)

    def publish(self, event: EventCreated) -> None:
        for subscriber in self._subscribers:
            subscriber.handle(event)

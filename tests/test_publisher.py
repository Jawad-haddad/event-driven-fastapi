from app.events import EventCreated
from app.publisher import EventPublisher, Subscriber


class Recorder(Subscriber):
    def __init__(self):
        self.received = []

    def handle(self, event):
        self.received.append(event)


def test_every_subscriber_receives_the_event():
    publisher = EventPublisher()
    first, second = Recorder(), Recorder()
    publisher.subscribe(first)
    publisher.subscribe(second)

    event = EventCreated.new("Concert", "a@b.com", "+962700000000")
    publisher.publish(event)

    assert first.received == [event]
    assert second.received == [event]


def test_publish_with_no_subscribers_does_nothing():
    EventPublisher().publish(EventCreated.new("Empty", "a@b.com", "1"))

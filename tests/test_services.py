from app.events import EventCreated
from app.notifications.channels import EmailChannel, NotificationChannel, SmsChannel
from app.subscribers.notification_service import NotificationService
from app.subscribers.ticket_service import TicketService

EVENT = EventCreated.new("Concert", "a@b.com", "+962700000000")


def test_notification_service_uses_every_channel():
    email, sms = EmailChannel(), SmsChannel()
    NotificationService([email, sms]).handle(EVENT)

    assert email.sent == ["[email] to a@b.com: 'Concert' was created"]
    assert sms.sent == ["[sms] to +962700000000: 'Concert' was created"]


def test_new_channel_needs_no_change_to_the_service():
    class TelegramChannel(NotificationChannel):
        name = "telegram"

        def recipient(self, event):
            return "@attendee"

    telegram = TelegramChannel()
    NotificationService([telegram]).handle(EVENT)

    assert telegram.sent == ["[telegram] to @attendee: 'Concert' was created"]


def test_ticket_service_reserves_once_per_event():
    service = TicketService()
    service.handle(EVENT)
    service.handle(EVENT)

    assert list(service.reservations) == [EVENT.event_id]

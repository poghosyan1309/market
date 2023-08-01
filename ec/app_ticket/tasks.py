from celery import shared_task
from django.conf import settings
from datetime import timedelta, datetime
from twilio.rest import Client
from app_ticket import models

@shared_task
def send_sms(phone, message):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )

@shared_task
def close_open_tickets():
    """
    Close tickets that are open before 24 hours
    And send SMS to the user to let them know that their ticket is closed.
    """

    tickets = models.Ticket.opentickets.filter(
        last_update__lte=datetime.now() - timedelta(hours=24),
    )

    for ticket in tickets:
        send_sms.delay(ticket.owner.phone, f'Your ticket with subject "{ticket.subject}" has been closed.')

    tickets.update(
        is_open=False,
        close_date=datetime.now(),
    )

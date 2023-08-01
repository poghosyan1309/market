import redis
import os
from celery import shared_task
from twilio.rest import Client
from dotenv import load_dotenv
from random import randint

from django.conf import settings
load_dotenv()


@shared_task
def send_sms_user_register(data):
    otp_code = randint(100000, 999999)
    user = {
        'otp_code': otp_code,
        'name': data['name'],
        'password': data['password'],
    }

    # Save the OTP code in your Redis database
    redis_con = redis.Redis(
        host=os.environ['REDIS_HOST'],
        port=int(os.environ['REDIS_PORT']),
        db=int(os.environ['PHONE_REGISTER_DB'])
    )
    redis_con.hset(data['phone'], mapping=user)
    redis_con.expire(data['phone'], settings.TIME_EXPIRE)

    # Set up the Twilio client

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    # Compose the SMS message
    message = client.messages.create(
        body=f'Your code is {otp_code}, time is {settings.TIME_EXPIRE} seconds',
        from_=os.environ['TWILIO_PHONE_NUMBER'],
        to=data['phone']
    )


@shared_task
def send_sms_forget_password(phone):
    otp_code = randint(100000, 999999)

    # Save the OTP code in your Redis database
    redis_con = redis.Redis(
        host=os.environ['REDIS_HOST'],
        port=int(os.environ['REDIS_PORT']),
        db=int(os.environ['FORGET_PASSWORD_DB'])
    )
    redis_con.set(phone, otp_code, settings.TIME_EXPIRE)

    # Set up the Twilio client and send the SMS (similar to your previous implementation)
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    # Compose the SMS message
    message = client.messages.create(
        body=f'Your code is {otp_code}, time is {settings.TIME_EXPIRE} seconds',
        from_=os.environ['TWILIO_PHONE_NUMBER'],
        to=phone
    )

    # You can check the status of the message if needed
    print(message.status)

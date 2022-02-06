from celery import shared_task
from django.core.mail import send_mail
from time import sleep

@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_email_task(email):
    send_mail('Welcome',
              'This is a greeting email from our side, welcome aboard.',
              'jhawar556shubh@gmail.com',
              [email])
    return None


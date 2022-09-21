from django.core.mail import send_mail
from celery import shared_task

from slack_sdk import WebClient
from django.conf import settings


slack_token = settings.SLACK_TOKEN
client = WebClient(token=slack_token)


@shared_task
def send_email(question, user, user_mail, to):
    subject = 'Request from ' + user
    message = question
    send_mail(subject, message, user_mail, [to])


@shared_task
def send_slack_msg(message, channel):
    client.chat_postMessage(
        channel=channel,
        text=message
    )


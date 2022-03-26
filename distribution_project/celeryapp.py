from __future__ import absolute_import, unicode_literals
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distribution_project.settings')
django.setup()

from django.db.models import ObjectDoesNotExist
from django.utils import timezone
from celery import Celery
from celery.schedules import crontab

from mainapp.models import SingleMessage
from mainapp.utils import send_mail_to_user


app = Celery('distribution_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(), periodic_check_of_sending.s())


@app.task(retry_kwargs={'max_retries': 5}, default_retry_delay=60)
def send_mail_task(message_id):
    try:
        message = SingleMessage.objects.select_related().get(pk=message_id)
    except ObjectDoesNotExist as e:
        print("Message with id={} doesn't exist!".format(message.pk))
    else:
        send_mail_to_user(message.client.email)
        message.status = SingleMessage.SENT
        message.save(update_fields=['status'])


@app.task
def periodic_check_of_sending():
    for message in SingleMessage.objects.select_related().filter(distribution__started_at__lte=timezone.now(),
                                                                 distribution__finished_at__gt=timezone.now(),
                                                                 status__in=[SingleMessage.NOT_SENT]):
        send_mail_to_user(message.client.email)
        message.status = SingleMessage.SENT
        message.save(update_fields=['status'])

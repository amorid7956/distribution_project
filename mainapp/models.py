# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models, transaction
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models import signals


class ClientManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given phone must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Client(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_staff = models.BooleanField(verbose_name='Может ли заходить в админку', default=False)

    USERNAME_FIELD = 'email'

    objects = ClientManager()

    def get_username(self):
        return self.email

    def get_short_name(self):
        return self.email

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return '{} | {}'.format(self.pk, self.email)


class Distribution(models.Model):
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время запуска рассылки')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время окончания рассылки')
    property_filter = models.CharField(max_length=256, null=True, blank=True, verbose_name='Фильтр свойств для клиентов')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return '{}'.format(self.pk)

    def send_mails_for_current_distribution(self):
        for client in Client.objects.filter(email__icontains=self.property_filter):
            message = SingleMessage.objects.create(distribution=self, client=client)
            print('Message with id={} was successfully created'.format(message.pk))


class SingleMessage(models.Model):
    SENT = 'sent'
    WAS_READ = 'was_read'
    NOT_SENT = 'not_sent'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (WAS_READ, 'Was_read'),
        (NOT_SENT, 'Not_sent'),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания сообщения')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=NOT_SENT)
    distribution = models.ForeignKey(Distribution, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return '{} | {} | {}'.format(self.pk, self.created_at, self.status)


def __message_post_save(sender, instance, created, **kwargs):
    if created:
        from distribution_project.celeryapp import send_mail_task
        if instance.distribution.started_at <= timezone.now() < instance.distribution.finished_at:
            send_mail_task.delay(instance.pk)


@receiver(signal=signals.post_save, sender=SingleMessage)
def message_post_save(sender, instance, created, **kwargs):
    transaction.on_commit(lambda: __message_post_save(sender, instance, created, **kwargs))

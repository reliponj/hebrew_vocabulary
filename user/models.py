import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    is_subscribe = models.BooleanField('Подписан?', default=False)
    sub_date = models.DateField('Дата подписки', null=True, blank=True)
    is_trial_used = models.BooleanField('Пробный период использован?', default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_sub_date(self):
        if not self.sub_date:
            return '-'
        return self.sub_date.strftime('%d.%m.%Y')

    def is_sub_active(self):
        if self.is_subscribe:
            return True

        now = timezone.now()
        if self.sub_date >= datetime.date(day=now.day, month=now.month, year=now.year):
            return True

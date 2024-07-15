from django.db import models


class Payment(models.Model):
    user = models.ForeignKey('user.User', verbose_name='Пользователь', on_delete=models.CASCADE)
    sum = models.IntegerField('Сумма', default=0)
    status = models.CharField('Статус', max_length=100, default='waiting')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return self.user.email

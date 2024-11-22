from django.db import models

class BinyanInApp(models.Model):
    binyan = models.CharField(max_length=20)
    text_ru = models.TextField(default='')
    text_ua = models.TextField(default='')
    text_en = models.TextField(default='')
    sort = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Биньян в приложении'
        verbose_name_plural = 'Биньяны в приложении'
        ordering = ['sort']

    def __str__(self):
        return self.binyan

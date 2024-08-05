from django.db import models


class Setting(models.Model):
    key_words = models.TextField('Ключевые слова', blank=True)
    text_ru = models.TextField('Текст (RU)', blank=True)
    text_ua = models.TextField('Текст (UA)', blank=True)
    text_en = models.TextField('Текст (EN)', blank=True)
    about_ru = models.TextField('Справка (RU)', blank=True, default='')
    about_ua = models.TextField('Справка (UA)', blank=True, default='')
    about_en = models.TextField('Справка (EN)', blank=True, default='')
    payment_sum = models.IntegerField('Сумма платежа', default=0)

    app_about_ru = models.TextField('Справка App (RU)', blank=True, default='')
    app_about_ua = models.TextField('Справка App (UA)', blank=True, default='')
    app_about_en = models.TextField('Справка App (EN)', blank=True, default='')
    app_about_il = models.TextField('Справка App (IL)', blank=True, default='')

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return 'Настройки'

    @staticmethod
    def get_settings():
        settings = Setting.objects.filter().first()
        if not settings:
            settings = Setting()
            settings.save()
        return settings


class Vocabulary(models.Model):
    root = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    binyan = models.CharField(max_length=255, blank=True, null=True)

    word = models.CharField(max_length=255)
    word_u = models.CharField(max_length=255)
    word_a = models.CharField(max_length=255)
    words2 = models.CharField(max_length=255, default='')
    words1 = models.CharField(max_length=255)
    words = models.CharField(max_length=255, null=True, blank=True)
    words_clear = models.CharField(max_length=255, null=True, blank=True)
    filter_for_app = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Vocabulary'
        verbose_name_plural = ' Vocabulary'
        ordering = ['root']

    def __str__(self):
        return self.root


class Spisok6(models.Model):
    roots = models.CharField(max_length=255)
    words = models.CharField(max_length=255)
    tables = models.IntegerField(default=0)
    tables_2 = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Spisok 6'
        verbose_name_plural = ' Spisok 6'
        ordering = ['tables', 'roots']


class Spisok1(models.Model):
    roots = models.CharField(max_length=255)
    words = models.CharField(max_length=255)
    word = models.CharField(max_length=255)
    r = models.CharField(max_length=100, null=True, blank=True)
    links = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Spisok 1'
        verbose_name_plural = ' Spisok 1'
        ordering = ['links']


class Group(models.Model):
    group = models.IntegerField()
    roots = models.ManyToManyField('Root', blank=True, related_name='groups')

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['group']

    def __str__(self):
        return str(self.group)


class Root(models.Model):
    root = models.CharField(max_length=50)
    number = models.IntegerField(default=10000)

    class Meta:
        verbose_name = 'Root'
        verbose_name_plural = 'Roots'
        ordering = ['root']

    def __str__(self):
        return self.root

    def get_binyans(self):
        binyans = []
        for bin in self.binyans.all():
            binyans.append(bin.binyan)
        return '  |  '.join(binyans)

    def get_groups(self):
        groups = []
        for group in self.groups.all():
            groups.append(str(group.group))
        return '  |  '.join(groups)


class Binyan(models.Model):
    root = models.ForeignKey('Root', related_name='binyans', on_delete=models.CASCADE, null=True)
    binyan = models.CharField(max_length=50)
    link = models.CharField(max_length=100, default='')

    class Meta:
        verbose_name = 'Binyan'
        verbose_name_plural = 'Binyans'
        ordering = ['link']

    def __str__(self):
        return self.binyan


class RCategory(models.Model):
    r = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'R-Category'
        verbose_name_plural = 'R-Categories'
        ordering = ['r']

    def __str__(self):
        return self.r


class Kluch(models.Model):
    value = models.CharField('Ключ', max_length=255)

    class Meta:
        verbose_name = 'Ключ'
        verbose_name_plural = 'Ключи'
        ordering = ['value']

    def __str__(self):
        return self.value

# Generated by Django 5.0.2 on 2024-07-15 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivrit', '0021_alter_root_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_words', models.TextField(blank=True, verbose_name='Ключевые слова')),
                ('text_ru', models.TextField(blank=True, verbose_name='Текст (RU)')),
                ('text_ua', models.TextField(blank=True, verbose_name='Текст (UA)')),
                ('text_en', models.TextField(blank=True, verbose_name='Текст (EN)')),
            ],
            options={
                'verbose_name': 'Настройки',
                'verbose_name_plural': 'Настройки',
            },
        ),
    ]
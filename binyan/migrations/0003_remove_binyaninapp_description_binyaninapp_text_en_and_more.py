# Generated by Django 5.0.2 on 2024-11-22 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binyan', '0002_alter_binyaninapp_options_binyaninapp_sort'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='binyaninapp',
            name='description',
        ),
        migrations.AddField(
            model_name='binyaninapp',
            name='text_en',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='binyaninapp',
            name='text_ru',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='binyaninapp',
            name='text_ua',
            field=models.TextField(default=''),
        ),
    ]

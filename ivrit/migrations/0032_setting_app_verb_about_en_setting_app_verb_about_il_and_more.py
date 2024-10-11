# Generated by Django 5.0.2 on 2024-10-07 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivrit', '0031_kluch_root'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='app_verb_about_en',
            field=models.TextField(blank=True, default='', verbose_name='Справка App Verb (EN)'),
        ),
        migrations.AddField(
            model_name='setting',
            name='app_verb_about_il',
            field=models.TextField(blank=True, default='', verbose_name='Справка App Verb (IL)'),
        ),
        migrations.AddField(
            model_name='setting',
            name='app_verb_about_ru',
            field=models.TextField(blank=True, default='', verbose_name='Справка App Verb (RU)'),
        ),
        migrations.AddField(
            model_name='setting',
            name='app_verb_about_ua',
            field=models.TextField(blank=True, default='', verbose_name='Справка App Verb (UA)'),
        ),
    ]
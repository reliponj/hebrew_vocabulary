# Generated by Django 5.0.2 on 2024-07-30 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivrit', '0025_vocabulary_words2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kluch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='Ключ')),
            ],
            options={
                'verbose_name': 'Ключ',
                'verbose_name_plural': 'Ключи',
            },
        ),
    ]

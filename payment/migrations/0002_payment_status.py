# Generated by Django 5.0.2 on 2024-07-15 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(default='waiting', max_length=100, verbose_name='Статус'),
        ),
    ]

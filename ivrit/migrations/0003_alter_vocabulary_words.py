# Generated by Django 5.0.2 on 2024-06-29 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivrit', '0002_root'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabulary',
            name='words',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

# Generated by Django 5.0.2 on 2024-07-02 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ivrit', '0015_binyan'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='binyan',
            options={'ordering': ['link'], 'verbose_name': 'Binyan', 'verbose_name_plural': 'Binyans'},
        ),
    ]

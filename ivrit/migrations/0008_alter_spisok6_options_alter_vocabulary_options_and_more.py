# Generated by Django 5.0.2 on 2024-06-30 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivrit', '0007_spisok6'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spisok6',
            options={'ordering': ['tables', 'roots'], 'verbose_name': 'Spisok 6', 'verbose_name_plural': 'Spisok 6'},
        ),
        migrations.AlterModelOptions(
            name='vocabulary',
            options={'ordering': ['root'], 'verbose_name': 'Vocabulary', 'verbose_name_plural': 'Vocabulary'},
        ),
        migrations.AddField(
            model_name='root',
            name='group',
            field=models.IntegerField(default=100000),
        ),
    ]

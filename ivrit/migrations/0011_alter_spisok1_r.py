# Generated by Django 5.0.2 on 2024-06-30 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivrit', '0010_spisok1_alter_rcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spisok1',
            name='r',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

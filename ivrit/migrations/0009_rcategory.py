# Generated by Django 5.0.2 on 2024-06-30 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivrit', '0008_alter_spisok6_options_alter_vocabulary_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'R-Category',
                'verbose_name_plural': 'R-Categories',
            },
        ),
    ]

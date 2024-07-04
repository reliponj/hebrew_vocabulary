# Generated by Django 5.0.2 on 2024-06-29 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivrit', '0004_binyan_root_binyans'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='root',
            options={'ordering': ['root'], 'verbose_name': 'Root', 'verbose_name_plural': 'Roots'},
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='binyan',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='link',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='root',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='word',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='word_a',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='word_u',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='words',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vocabulary',
            name='words1',
            field=models.CharField(max_length=100),
        ),
    ]

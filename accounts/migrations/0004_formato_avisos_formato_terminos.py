# Generated by Django 5.0.6 on 2024-06-28 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_formato_emision'),
    ]

    operations = [
        migrations.AddField(
            model_name='formato',
            name='avisos',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='formato',
            name='terminos',
            field=models.TextField(blank=True),
        ),
    ]

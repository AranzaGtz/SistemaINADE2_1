# Generated by Django 5.1 on 2024-09-09 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizacion',
            name='rfc',
            field=models.CharField(default=0, max_length=13, unique=True),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.0.7 on 2024-08-07 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_informacioncontacto_celular_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="informacioncontacto",
            name="telefono",
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]

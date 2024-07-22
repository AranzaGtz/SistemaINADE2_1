# Generated by Django 5.0.7 on 2024-07-22 14:32

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormatoCotizacion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre_formato", models.CharField(max_length=255)),
                ("version", models.CharField(max_length=50)),
                ("emision", models.DateField(default=django.utils.timezone.now)),
                ("terminos", models.TextField(blank=True)),
                ("avisos", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="FormatoOrden",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre_formato", models.CharField(max_length=255)),
                ("version", models.CharField(max_length=50)),
                ("emision", models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name="organizacion",
            name="f_cotizacion",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="formatos",
                to="accounts.formatocotizacion",
            ),
        ),
        migrations.AddField(
            model_name="organizacion",
            name="f_orden",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="formatos",
                to="accounts.formatoorden",
            ),
        ),
    ]

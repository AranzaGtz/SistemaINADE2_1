# Generated by Django 5.0.7 on 2024-08-15 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_alter_cotizacion_fecha_solicitud_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cotizacion",
            name="tasa_iva",
            field=models.CharField(
                choices=[("0.08", "8%"), ("0.16", "16%")], default="0.08", max_length=4
            ),
        ),
    ]

# Generated by Django 5.0.7 on 2024-07-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_cotizacion_cotizacion_pdf_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cotizacion",
            name="orden_perdon_pdf",
            field=models.FileField(
                blank=True, null=True, upload_to="ordenes_pedido_pdfs/"
            ),
        ),
    ]

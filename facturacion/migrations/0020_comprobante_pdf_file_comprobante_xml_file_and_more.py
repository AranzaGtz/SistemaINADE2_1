# Generated by Django 5.1 on 2024-10-08 18:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0019_alter_comprobante_metodo_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprobante',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='cfdis/pdf/'),
        ),
        migrations.AddField(
            model_name='comprobante',
            name='xml_file',
            field=models.FileField(blank=True, null=True, upload_to='cfdis/xml/'),
        ),
        migrations.AlterField(
            model_name='comprobante',
            name='factura',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comprobantes', to='facturacion.factura'),
        ),
    ]

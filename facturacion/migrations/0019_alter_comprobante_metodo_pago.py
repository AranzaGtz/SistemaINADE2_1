# Generated by Django 5.1 on 2024-10-07 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0018_alter_comprobante_cfdi_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprobante',
            name='metodo_pago',
            field=models.CharField(choices=[('01', 'Efectivo'), ('02', 'Cheque Nominativo'), ('03', 'Transferencia electrónica de fondos')], default='03', max_length=5),
        ),
    ]

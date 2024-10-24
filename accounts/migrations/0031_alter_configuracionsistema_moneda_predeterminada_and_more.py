# Generated by Django 5.1 on 2024-10-18 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_remove_cotizacion_t_cambio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracionsistema',
            name='moneda_predeterminada',
            field=models.CharField(choices=[('MXN', 'MXN - Moneda Nacional Mexicana')], default='MXN', max_length=10, verbose_name='Moneda Predeterminada'),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='metodo_pago',
            field=models.CharField(choices=[('MXN', 'MXN - Moneda Nacional Mexicana')], max_length=100),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='moneda',
            field=models.CharField(blank=True, choices=[('MXN', 'MXN - Moneda Nacional Mexicana')], max_length=10, null=True),
        ),
    ]

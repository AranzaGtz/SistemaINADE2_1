# Generated by Django 5.1 on 2024-09-04 18:38

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moneda_predeterminada', models.CharField(choices=[('MXN', 'MXN - Moneda Nacional Mexicana'), ('USD', 'USD - Dolar Estadunidense')], default='MXN', max_length=10, verbose_name='Moneda Predeterminada')),
                ('tasa_iva_default', models.CharField(choices=[('0.08', '8%'), ('0.16', '16%')], default='0.08', max_length=4, verbose_name='Tasa de IVA Predeterminada')),
                ('formato_numero_cotizacion', models.CharField(choices=[('COT-{year}-{seq}', 'COT-{year}-{seq}'), ('{year}-COT-{seq}', '{year}-COT-{seq}'), ('COT-{seq}', 'COT-{seq}'), ('{seq}', '{seq}')], default='{seq}', max_length=50, verbose_name='Formato de Número de Cotización')),
            ],
            options={
                'verbose_name': 'Configuración del Sistema',
                'verbose_name_plural': 'Configuraciones del Sistema',
            },
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_personalizado', models.CharField(blank=True, max_length=4, null=True, unique=True)),
                ('fecha_solicitud', models.DateField(blank=True, null=True)),
                ('fecha_caducidad', models.DateField(blank=True, null=True)),
                ('metodo_pago', models.CharField(choices=[('MXN', 'MXN - Moneda Nacional Mexicana'), ('USD', 'USD - Dolar Estadunidense')], max_length=100)),
                ('tasa_iva', models.CharField(choices=[('0.08', '8%'), ('0.16', '16%')], max_length=4)),
                ('notas', models.TextField(blank=True, null=True)),
                ('correos_adicionales', models.TextField(blank=True, null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('iva', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('estado', models.BooleanField(default=False)),
                ('cotizacion_pdf', models.FileField(blank=True, null=True, upload_to='cotizaciones_pdfs/')),
                ('orden_pedido_pdf', models.FileField(blank=True, null=True, upload_to='ordenes_pedido_pdfs/')),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('calle', models.CharField(max_length=50)),
                ('numero', models.CharField(max_length=50)),
                ('colonia', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=6)),
                ('estado', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FormatoCotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_formato', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=50)),
                ('emision', models.DateField(default=django.utils.timezone.now)),
                ('titulo_documento', models.CharField(blank=True, default='COTIZACIÓN / CONTRATO', max_length=255)),
                ('mensaje_propuesta', models.TextField(blank=True, default='Gracias por la oportunidad de presentar nuestra propuesta. Por favor revise que se cumple con sus requerimientos; en caso contrario, comuníquese con nosotros.')),
                ('terminos', models.TextField(blank=True)),
                ('avisos', models.TextField(blank=True)),
                ('imagen_marca_agua', models.ImageField(blank=True, null=True, upload_to='marca_agua/')),
            ],
        ),
        migrations.CreateModel(
            name='FormatoOrden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_formato', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=50)),
                ('emision', models.DateField(default=django.utils.timezone.now)),
                ('titulo_documento', models.CharField(blank=True, default='Orden de Trabajo', max_length=255)),
                ('imagen_marca_agua', models.ImageField(blank=True, null=True, upload_to='marca_agua/')),
            ],
        ),
        migrations.CreateModel(
            name='InformacionContacto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('telefono', models.CharField(blank=True, max_length=120, null=True)),
                ('celular', models.CharField(blank=True, max_length=20, null=True)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Metodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metodo', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Queja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('asunto', models.CharField(max_length=200)),
                ('mensaje', models.TextField()),
                ('prioridad', models.CharField(choices=[('Baja', 'Baja'), ('Media', 'Media'), ('Alta', 'Alta')], max_length=50)),
                ('archivo_adjunto', models.FileField(blank=True, null=True, upload_to='soporte_adjuntos/')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=50)),
                ('abreviatura', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('celular', models.CharField(blank=True, max_length=15, null=True)),
                ('rol', models.CharField(blank=True, choices=[('admin', 'Administrador'), ('coordinador', 'Coordinador'), ('muestras', 'Muestras'), ('informes', 'Informes'), ('laboratorio', 'Laboratorio'), ('calidad', 'Calidad')], default='admin', max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Concepto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_servicios', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('importe', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('notas', models.TextField(blank=True, null=True)),
                ('subcontrato', models.BooleanField(default=False)),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conceptos', to='accounts.cotizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_empresa', models.CharField(max_length=100)),
                ('rfc', models.CharField(blank=True, max_length=50, null=True)),
                ('moneda', models.CharField(blank=True, choices=[('MXN', 'MXN - Moneda Nacional Mexicana'), ('USD', 'USD - Dolar Estadunidense')], max_length=10, null=True)),
                ('condiciones_pago', models.CharField(blank=True, default='15', max_length=200)),
                ('direccion', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.direccion')),
            ],
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
                ('mensaje', models.TextField()),
                ('enlace', models.URLField()),
                ('leido', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.CreateModel(
            name='OrdenTrabajo',
            fields=[
                ('id_personalizado', models.CharField(blank=True, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('estado', models.BooleanField(default=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('gestion', models.BooleanField(default=False)),
                ('orden_trabajo_pdf', models.FileField(blank=True, null=True, upload_to='ordenes_trabajo_pdfs/')),
                ('cotizacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orden_trabajo', to='accounts.cotizacion')),
                ('direccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordenes_trabajo', to='accounts.direccion')),
                ('receptor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ordenes_trabajo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenTrabajoConcepto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.concepto')),
                ('orden_de_trabajo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conceptos', to='accounts.ordentrabajo')),
            ],
        ),
        migrations.CreateModel(
            name='Organizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Ingenieria y Administración Estratégica, S.A. de C.V.', max_length=255)),
                ('slogan', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion', models.CharField(default='Calle Puebla, No. 4990, col. Guillen, Tijuana BC, México, C.P. 22106', max_length=255)),
                ('telefono', models.CharField(default='(664) 104 51 44', max_length=20)),
                ('pagina_web', models.URLField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('f_cotizacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='formatos', to='accounts.formatocotizacion')),
                ('f_orden', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='formatos', to='accounts.formatoorden')),
            ],
        ),
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Matriz', max_length=255)),
                ('direccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='almacen_direccion', to='accounts.direccion')),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='almacen_sucursal', to='accounts.organizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.empresa')),
                ('informacion_contacto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.informacioncontacto')),
                ('titulo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.titulo')),
            ],
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='accounts.persona'),
        ),
        migrations.CreateModel(
            name='Prospecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prospecto', to='accounts.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=15)),
                ('nombre_servicio', models.CharField(max_length=100)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.TextField()),
                ('unidad', models.CharField(max_length=50)),
                ('unidad_cfdi', models.CharField(choices=[('ACT', 'ACT - Actividad'), ('E48', 'E48 - Unidad de Servicio'), ('H87', 'H87 - Pieza'), ('EA', 'EA - Elemento'), ('E51', 'E51 - Trabajo')], default='E48', max_length=20)),
                ('clave_cfdi', models.CharField(choices=[('77101700', '77101700 - Servicios de asesoría ambiental'), ('77101701', '77101701 - Servicios de asesoramiento sobre ciencias ambientales')], default='77101700', max_length=20)),
                ('subcontrato', models.BooleanField(default=False)),
                ('acreditado', models.BooleanField(default=True)),
                ('metodo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.metodo')),
            ],
        ),
        migrations.AddField(
            model_name='concepto',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.servicio'),
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='Matriz', max_length=255)),
                ('direccion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sucursal_direccion', to='accounts.direccion')),
                ('organizacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='organizacion_sucursal', to='accounts.organizacion')),
            ],
        ),
    ]
